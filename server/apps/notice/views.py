from django.shortcuts import render, redirect, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Notice, Appendix, announce_time
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from server.settings import RESOURCES_DIR
from utils.FileUtil import *
from utils.EmailUtil import EmailUtil
from apps.user.models import Student
import datetime
# Create your views here.


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


def add_job(func, trigger='date', job_args=[], job_id='job', rundate=datetime.datetime.now()):
    try:
        scheduler.add_job(
            func,
            trigger,
            args=job_args,
            id=job_id,
            run_date=rundate
        )
    except Exception as e:
        print(e)
        scheduler.shutdown()


def index(request):
    notice_list = Notice.objects.order_by("-update_at").all()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    return render(
        request,
        'notice/index.html',
        {"notices": get_page(notice_list, page), "len": len(notice_list)}
    )


def detail(request, n_id):
    ntc = Notice.objects.filter(id=n_id)
    if len(ntc) == 1:
        return render(
            request,
            'notice/detail.html',
            {
                "notice": ntc[0],
                "file_count": len(ntc[0].appendix.file_list),
                "now": datetime.datetime.now()
            }
        )
    return HttpResponse(status=404)


def alert(account, identity, n_id):
    students = Student.objects.all()
    rcp_list = []
    for stu in students:
        if stu.email != '':
            rcp_list.append(stu.email)
    manager = EmailUtil(
        account=account,
        identity=identity,
        receive=rcp_list,
        notice_id=n_id
    )
    manager.send("notice")


def create(request):
    new_id = 1
    n_all = Notice.objects.all()
    if len(n_all) > 0:
        new_id = n_all[len(n_all) - 1].pk + 1
    if request.method == 'GET':
        make_dir(os.path.join(RESOURCES_DIR, 'notice', str(new_id)))
        return render(
            request,
            'notice/create.html',
            {
                "default_time": announce_time().strftime('%Y-%m-%d %H:%M:%S'),
                "now": datetime.datetime.now()
            }
        )
    if request.method == 'POST':
        file_count = int(request.POST.get("appendix"))
        appended = []
        for count in range(file_count):
            file = request.FILES["file_" + str(count)]
            saved_path = os.path.join(
                RESOURCES_DIR,
                'notice',
                str(new_id),
                file.name
            )
            write_file(file, saved_path)
            stuffix = os.path.splitext(file.name)[1]
            appended.append({"stuffix": stuffix, "filename": file.name, "saved_path": saved_path})
        apdix = Appendix(
            id=new_id,
            file_list=appended
        )
        apdix.save()
        title = request.POST.get("title")
        content = request.POST.get("content")
        announce_at = datetime.datetime.strptime(
            request.POST.get("announce_at"),
            "%Y-%m-%d %H:%M:%S"
        )
        email_alert = request.POST.get("email_alert") == 'true'
        notice = Notice(
            id=new_id,
            publisher=request.session.get("account"),
            title=title,
            content=content,
            appendix=apdix,
            announce_at=announce_at,
            email_alert=email_alert,
            with_appendix=file_count > 0
        )
        notice.save()
        if email_alert:
            ac = request.session.get("account")
            iden = request.session.get("identity")
            n_id = notice.id
            add_job(
                alert,
                "date",
                job_args=[ac, iden, n_id],
                job_id=str(n_id) + '_alert',
                rundate=announce_at
            )
        return JsonResponse({"msg": "done"})
    return HttpResponse(status=500)


@require_http_methods(["POST"])
def modify(request, n_id):
    ntc = Notice.objects.filter(id=n_id)
    if len(ntc) == 1:
        if request.POST.get("operation") == "remove":
            for f in ntc[0].appendix.file_list:
                remove_file(f["saved_path"])
            os.rmdir(
                os.path.join(
                    RESOURCES_DIR,
                    'notice',
                    str(ntc[0].id)
                )
            )
            ntc[0].appendix.delete()
            ntc.delete()
            job = scheduler.get_job(job_id=str(n_id) + '_alert')
            if job:
                scheduler.remove_job(str(n_id) + "_alert")
            return JsonResponse({"msg": "done"})
        with_appendix = ntc[0].with_appendix
        appendix = ntc[0].appendix
        if request.POST.get("operation") == "clear_appendix":
            make_dir(
                os.path.join(RESOURCES_DIR, "notice", str(n_id))
            )
            appendix.file_list.clear()
            with_appendix = False
            appendix.save()
            ret = ntc.update(
                with_appendix=with_appendix,
                appendix=appendix
            )
            if ret == 1:
                return JsonResponse({"msg": "done"})
            return HttpResponse(status=500)
        if request.POST.get("operation") == "add_appendix":
            with_appendix = True
            file_count = int(request.POST.get("appendix"))
            for count in range(file_count):
                file = request.FILES["file_" + str(count)]
                saved_path = os.path.join(
                    RESOURCES_DIR,
                    'notice',
                    str(n_id),
                    file.name
                )
                stuffix = os.path.splitext(file.name)[1]
                write_file(file, saved_path)
                appendix.file_list.append({"stuffix": stuffix, "filename": file.name, "saved_path": saved_path})
            appendix.save()
            # return JsonResponse({"msg": "done"})
        title = request.POST.get("title")
        content = request.POST.get("content")
        email_alert = request.POST.get("email_alert") == 'true'
        announce_at = datetime.datetime.strptime(
            request.POST.get("announce_at"),
            "%Y-%m-%d %H:%M:%S"
        )
        job = scheduler.get_job(job_id=str(n_id) + '_alert')
        if email_alert:
            if job:
                if job.next_run_time != announce_at:
                    job.modify(
                        run_date=announce_at
                    )
            else:
                ac = request.session.get("account")
                iden = request.session.get("identity")
                n_id = ntc[0].id
                add_job(
                    alert,
                    "date",
                    job_args=[ac, iden, n_id],
                    job_id=str(n_id) + '_alert',
                    rundate=announce_at
                )
        else:
            if job:
                scheduler.remove_job(str(n_id) + "_alert")
        ret = ntc.update(
            title=title,
            content=content,
            announce_at=announce_at,
            email_alert=email_alert,
            with_appendix=with_appendix,
            appendix=appendix
        )
        if ret == 1:
            return JsonResponse({"msg": "done"})
    return HttpResponse(status=404)


@require_http_methods(["GET"])
def get_appendix(request, n_id):
    notice = Notice.objects.filter(id=n_id)
    if len(notice) == 1:
        num = int(request.GET.get("apd"))
        path = notice[0].appendix.file_list[num].get("saved_path")
        resp = download_response(path)
        return resp
    return HttpResponse(status=404)


def get_page(obj_list, page):
    paginator = Paginator(obj_list, 10)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except InvalidPage:
        pass
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


register_events(scheduler)
scheduler.start()
