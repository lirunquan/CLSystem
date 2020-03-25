from django.shortcuts import render, redirect, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import JsonResponse, FileResponse
from django.views.decorators.http import require_http_methods
from utils.FileUtil import *
from record.models import CommitMissionRecord
from server.settings import RESOURCES_DIR
from .models import Mission, end_time
import datetime
import pytz
# Create your views here.


def index(request):
    page = int(request.GET.get("page")) if request.GET.get("page") else 1
    mission_list = Mission.objects.order_by('-start_at').all()
    return render(
        request,
        'mission/index.html',
        {
            "mission_page": get_page(mission_list, page),
            "len": len(mission_list)
        }
    )


def detail(request, m_id):
    mission = Mission.objects.filter(id=m_id)
    account = request.session.get("account")
    commit_record = CommitMissionRecord.objects.filter(mission_id=m_id, account=account)
    has_committed = False
    if len(commit_record) > 0:
        has_committed = True
    if len(mission) == 1:
        now = datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))
        overtime = False
        if now > mission[0].end_at:
            overtime = True
        return render(
            request,
            'mission/detail.html',
            {"mission": mission[0],
             "committed": has_committed,
             "overtime": overtime}
        )
    return HttpResponse(status=404)


def create(request):
    if request.method == 'GET':
        new_id = 1
        m_all = Mission.objects.all()
        if len(m_all) > 0:
            new_id = m_all[len(m_all) - 1].id + 1
        make_dir(os.path.join(RESOURCES_DIR, 'mission', str(new_id)))
        start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        end = end_time().strftime("%Y-%m-%d %H:%M:%S")
        return render(
            request,
            'mission/create.html',
            {"start": start, "end": end}
        )
    if request.method == 'POST':
        title = request.POST.get("title")
        content = request.POST.get("content")
        start_at = datetime.datetime.strptime(
            request.POST.get("start_at"),
            "%Y-%m-%d %H:%M:%S"
        )
        end_at = datetime.datetime.strptime(
            request.POST.get("end_at"),
            "%Y-%m-%d %H:%M:%S"
        )
        if end_at < datetime.datetime.now():
            return JsonResponse({"msg": "invalid end time"})
        mis = Mission(
            publisher=request.session.get("account"),
            title=title,
            content=content,
            start_at=start_at,
            end_at=end_at
        )
        mis.save()
        return JsonResponse({"msg": "done"})
    return JsonResponse({"msg": "failed"})


@require_http_methods(['POST'])
def commit(request, m_id):
    mission = Mission.objects.filter(id=m_id)
    if len(mission) == 1:
        account = request.session.get("account")
        save_dir = os.path.join(RESOURCES_DIR, 'mission', str(m_id), account)
        make_dir(save_dir)
        file = request.FILES["zip_file"]
        saved_path = os.path.join(
            save_dir,
            file.name
        )
        write_file(file, saved_path)
        commited_record = CommitMissionRecord.objects.filter(mission_id=m_id, account=account)
        if len(commited_record) > 0:
            ret = commited_record.update(saved_path=saved_path)
            if ret == 1:
                return redirect('/mission/' + str(m_id) + '/detail')
        record = CommitMissionRecord(
            account=account,
            mission_id=m_id,
            saved_path=saved_path
        )
        record.save()
        return redirect('/mission/' + str(m_id) + '/detail')
    return HttpResponse(status=404)


def modify(request, m_id):
    mission = Mission.objects.filter(id=m_id)
    if len(mission) == 1:
        if request.POST.get("operation") == "remove":
            make_dir(
                os.path.join(
                    RESOURCES_DIR,
                    'mission',
                    str(mission[0].id)
                )
            )
            os.rmdir(
                os.path.join(RESOURCES_DIR, 'mission', str(mission[0].id))
            )
            mission.delete()
            return JsonResponse({"msg": "done"})
        title = request.POST.get("title")
        content = request.POST.get("content")
        start_at = datetime.datetime.strptime(
            request.POST.get("start_at"), "%Y-%m-%d %H:%M:%S"
        )
        end_at = datetime.datetime.strptime(
            request.POST.get("end_at"), "%Y-%m-%d %H:%M:%S"
        )
        ret = mission.update(
            title=title,
            content=content,
            start_at=start_at,
            end_at=end_at
        )
        if ret == 1:
            return JsonResponse({"msg": "done"})
        return JsonResponse({"msg": "failed"})
    return HttpResponse(status=404)


def get_commit(request, m_id):
    account = request.GET.get("account")
    record = CommitMissionRecord.objects.order_by('-time').filter(account=account, mission_id=m_id)
    path = record[0].saved_path
    f = open(path, 'rb')
    resp = FileResponse(f)
    resp["Content-Type"] = "application/octet-stream"
    disp = 'attachment;filename=' + path.split(os.path.sep)[-1] + '"'
    resp["Content-Disposition"] = disp
    return resp


def check_commit(request, m_id):
    mission = Mission.objects.filter(id=m_id)
    page = int(request.GET.get("page")) if request.GET.get("page") else 1
    if len(mission) != 1:
        return HttpResponse(status=404)
    records = CommitMissionRecord.objects.order_by('-time').filter(mission_id=m_id)
    return render(
        request,
        'mission/check.html',
        {"commit_list": get_page(records, page), "mission": mission[0]}
    )


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
