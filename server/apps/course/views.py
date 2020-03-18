from django.shortcuts import render, redirect, HttpResponse
from django.http import FileResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from .models import Chapter, Mission, Notice, Appendix, announce_time
from apps.record.models import CommitMissionRecord
from apps.user.models import Student
from server.settings import RESOURCES_DIR
from utils.FileUtil import *
from utils.EmailUtil import EmailUtil
import os
import time
import datetime
# Create your views here.


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


def index(request):
    chapter_list = Chapter.objects.all().order_by("chapter_num")
    chapter_num = 1
    if request.GET.get("chapter_num"):
        chapter_num = int(request.GET.get("chapter_num"))
    chapter_to_show = Chapter.objects.filter(chapter_num=chapter_num)
    return render(
        request,
        'course/course_index.html',
        {"chapter_list": chapter_list, "chapter_to_show": chapter_to_show}
    )


def chapter_create(request):
    if request.method == 'GET':
        return render(request, 'course/chapter_create.html')
    if request.method == 'POST':
        chapter_num = request.POST.get("chapter_num")
        title = request.POST.get("title")
        courseware_type = request.POST.get("courseware_type")
        couseware_file = request.FILES.get("courseware_file")
        filename = str(couseware_file.name)
        saved_dir = os.path.join(RESOURCES_DIR, 'course', str(chapter_num))
        make_dir(saved_dir)
        courseware_path = os.path.join(
            saved_dir,
            filename
        )
        write_file(couseware_file, courseware_path)
        chapter = Chapter(
            title=title,
            chapter_num=chapter_num,
            courseware_type=courseware_type,
            courseware_path=courseware_path,
        )
        chapter.save()
        return JsonResponse({"msg": "done"})
        # return HttpResponse(status=200)


def chapter_index(request, c_id):
    chapter = Chapter.objects.filter(id=c_id)
    if len(chapter) == 1:
        render(
            request,
            'course/chapter_index.html',
            {"chapter": chapter[0]}
        )
    return HttpResponse(status=404)


@require_http_methods(['POST'])
def chapter_modify(request, c_id):
    chapter = Chapter.objects.filter(id=c_id)
    courseware_file = request.POST.get("courseware_file")
    if len(chapter) == 1:
        if request.POST.get("operation") == "remove":
            chapter.delete()
            return JsonResponse({"msg": "done"})
        c_path = chapter[0].courseware_path
        if courseware_file:
            make_dir(os.path.dirname(chapter[0].courseware_path))
            saved_path = os.path.join(
                RESOURCES_DIR,
                'course',
                str(chapter[0].chapter_num),
                courseware_file.name
            )
            write_file(courseware_file, saved_path)
            c_path = saved_path
        ret = chapter.update(
            title=request.POST.get("title"),
            courseware_type=request.POST.get("courseware_type"),
            courseware_path=c_path
        )
        if ret == 1:
            return JsonResponse({"msg": "done"})
    return JsonResponse({"msg": "failed"})


@require_http_methods(["GET"])
def get_courseware(request, c_id):
    chapter = Chapter.objects.filter(id=c_id)
    if len(chapter) == 1:
        filepath = chapter[0].courseware_path
        f = open(filepath, 'rb')
        response = FileResponse(f)
        response["Content-Type"] = 'application/octet-stream'
        disp = 'attachment;filename="' + filepath.split(os.path.sep)[-1] + '"'
        response['Content-Disposition'] = disp
        return response
    return HttpResponse(status=404)


def notice_create(request):
    new_id = 1
    if request.method == 'GET':
        new_id = len(Notice.objects.all()) + 1
        make_dir(os.path.join(RESOURCES_DIR, 'notice', str(new_id)))
        return render(
            request,
            'course/notice_create.html',
            {"id": new_id, "default_time": announce_time().strftime('%Y-%m-%d %H:%M:%S')}
        )
    if request.method == 'POST':
        file_count = int(request.POST.get("appendix"))
        appended = []
        for count in range(file_count):
            file = request.FILES.get("file_" + str(count))
            saved_path = os.path.join(
                RESOURCES_DIR,
                'notice',
                str(new_id),
                file.name
            )
            write_file(file, saved_path)
            stuffix = os.path.splitext(file.name)[1]
            appended.append({"stuffix": stuffix, "saved_path": saved_path})
        apdix = Appendix(
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
            title=title,
            content=content,
            appendix=apdix,
            announce_at=announce_at,
            email_alert=email_alert,
            with_appendix=file_count > 0
        )
        notice.save()
        if email_alert:
            try:
                ac = request.session.get("account")
                iden = request.session.get("identity")
                n_id = notice.id
                scheduler.add_job(
                    alert,
                    "date",
                    run_date=notice.announce_at,
                    args=[ac, iden, n_id],
                    id=str(n_id) + '_alert'
                )
            except Exception as e:
                print(e)
                scheduler.shutdown()
                # return JsonResponse({"msg": "email error"})
        return JsonResponse({"msg": "done"})
    return HttpResponse(status=200)


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


def notice_index(request):
    notice_list = Notice.objects.order_by("-announce_at").all()
    return render(
        request,
        'course/notice_index.html',
        {"notices": notice_list}
    )


def notice_detail(request, n_id):
    ntc = Notice.objects.filter(id=n_id)
    if len(ntc) == 1:
        return render(
            request,
            'course/notice_detail.html',
            {"notice": ntc[0]}
        )
    return HttpResponse(status=404)


@require_http_methods(["POST"])
def notice_modify(request, n_id):
    ntc = Notice.objects.filter(id=n_id)
    if len(ntc) == 1:
        if request.POST.get("operation") == "remove":
            ntc.delete()
            return JsonResponse({"msg": "done"})
        with_appendix = ntc[0].with_appendix
        appendix = ntc[0].appendix
        if request.POST.get("operation") == "clear_appendix":
            for obj in appendix.file_list:
                remove_file(obj["saved_path"])
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
                file = request.FILES.get("file_" + str(count))
                saved_path = os.path.join(
                    RESOURCES_DIR,
                    'notice',
                    str(n_id),
                    file.name
                )
                stuffix = os.path.splitext(file.name)[1]
                write_file(file, saved_path)
                appendix.file_list.append({"stuffix": stuffix, "saved_path": saved_path})
            appendix.save()
            # return JsonResponse({"msg": "done"})
        title = request.POST.get("title")
        content = request.POST.get("content")
        email_alert = request.POST.get("email_alert") == 'true'
        announce_at = datetime.datetime.strptime(
            request.POST.get("announce_at"),
            "%Y-%m-%d %H:%M:%S"
        )
        if email_alert:
            job = scheduler.get_job(job_id=str(n_id) + '_alert')
            if job:
                if job.next_run_time != announce_at:
                    job.modify(next_run_time=announce_at)
            else:
                try:
                    ac = request.session.get("account")
                    iden = request.session.get("identity")
                    n_id = ntc[0].id
                    scheduler.add_job(
                        alert,
                        "date",
                        run_date=announce_at,
                        args=[ac, iden, n_id],
                        id=str(n_id) + '_alert'
                    )
                except Exception as e:
                    print(e)
                    scheduler.shutdown()
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
        f = open(path, 'rb')
        resp = FileResponse(f)
        resp["Content-Type"] = "application/octet-stream"
        filename = path.split(os.path.sep)[-1]
        disp = 'attachment;filename="' + filename + '"'
        resp["Content-Disposition"] = disp
        return resp
    return HttpResponse(status=404)


def mission_create(request):
    return HttpResponse(status=200)


def mission_index(request):
    return HttpResponse(status=200)


def mission_detail(requset, m_id):
    return HttpResponse(status=200)


def mission_modify(request, m_id):
    return HttpResponse(status=200)


def mission_commit(request, m_id):
    return HttpResponse(status=200)


def check_commit(request):
    m_id = int(request.GET.get("mission"))
    mission = Mission.objects.get(id=m_id)
    records = CommitMissionRecord.objects.order_by('-time').filter(mission_id=m_id)
    return render(
        request,
        'course/mission_check.html',
        {"commit_list": records, "mission": mission}
    )


def get_mission_upload(request):
    account = request.GET.get("account")
    m_id = int(request.GET.get("mission"))
    record = CommitMissionRecord.objects.order_by('-time').filter(account=account, mission_id=m_id)
    path = record[0].saved_path
    f = open(path, 'rb')
    resp = FileResponse(f)
    resp["Content-Type"] = "application/octet-stream"
    disp = 'attachment;filename=' + path.split(os.path.sep)[-1] + '"'
    resp["Content-Disposition"] = disp
    return resp


register_events(scheduler)
scheduler.start()
# print(
#     type(
#         scheduler.get_job(job_id='remove_overdue_record').next_run_time
#     )
# )
# scheduler.print_jobs()
