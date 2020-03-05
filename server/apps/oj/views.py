from django.shortcuts import render, redirect, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import FileResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Programme, Choice
from apps.record.models import CommitCodeRecord, CommitChoiceRecord
from server.settings import RESOURCES_DIR
from utils.FileUtil import *
from utils.JudgerUtil import JudgerUtil
from django_q.tasks import async_task
import json
import os
import time
# Create your views here.


def problems_list(request):
    prog_all = Programme.objects.all()
    choice_all = Choice.objects.all()
    if request.method == 'GET':
        p_page = int(request.GET.get('p_page')) if request.GET.get('p_page') else 1
        c_page = int(request.GET.get('c_page')) if request.GET.get('c_page') else 1
        prog_data = get_data(prog_all, p_page)
        choice_data = get_data(choice_all, c_page)
        return render(
            request,
            'oj/problems_list.html',
            {
                "p_data": prog_data,
                "c_data": choice_data
            })


def add_programme(request):
    if request.method == 'GET':
        return render(request, 'oj/programme_create.html')
    if request.method == 'POST':
        title = request.POST.get("title")
        detail = request.POST.get("detail")
        input_desc = request.POST.get("input_desc")
        output_desc = request.POST.get("output_desc")
        input_demo = request.POST.get("input_demo")
        output_demo = request.POST.get("output_demo")
        testcase_count = request.POST.get("testcase_count")
        testcase_file = request.FILES.get("testcase_zip")
        time_limit = request.POST.get("time_limit")
        memory_limit = request.POST.get("memory_limit")
        p_id = len(Programme.objects.all()) + 1
        tc_dir = os.path.join(RESOURCES_DIR, 'programme', 'testcase', str(p_id))
        save_tc_file(testcase_file, tc_dir)
        p = Programme(
            title=title,
            detail=detail,
            input_desc=input_desc,
            output_desc=output_desc,
            input_demo=input_demo,
            output_demo=output_demo,
            time_limit=time_limit,
            memory_limit=memory_limit,
            testcase_count=testcase_count,
            testcase_dir=tc_dir
        )
        p.save()
        make_dir(os.path.join(RESOURCES_DIR, 'programme', 'commit', str(p.id)))
        time.sleep(2)
        return JsonResponse({"msg": "done"})


def add_choice(request):
    return render(request, "oj/choice_create.html")


@require_http_methods(['POST'])
def add_choice_single(request):
    data_dic = json.loads(request.body)
    c = Choice(
        title=data_dic["title"],
        detail=data_dic["detail"],
        options=data_dic["options"],
        multichoice=data_dic["multichoice"],
        reference=data_dic["reference"]
    )
    c.save()
    return HttpResponse(status=200)


@require_http_methods(['POST'])
def add_choice_batch(request):
    execel_file = request.FILES.get("excel")
    filename = "upload_" + str(time.time()).replace('.', '') + '.xls'
    saved_path = os.path.join(RESOURCES_DIR, 'choices', filename)
    write_file(execel_file, saved_path)
    choices_list = handle_choice_excel(saved_path)
    for c in choices_list:
        options = {
            "A": c["A"],
            "B": c["B"],
            "C": c["C"],
            "D": c["D"]
        }
        choice = Choice(
            title=c["title"],
            detail=c["detail"],
            options=options,
            multichoice=c["multichoice"] == 'Y',
            reference=c["reference"]
        )
        choice.save()
    return redirect("/oj/problems_list")


@require_http_methods(['GET'])
def download_template(request):
    choice_temp_path = os.path.join(RESOURCES_DIR, 'choices', 'template.xls')
    f = open(choice_temp_path, 'rb')
    response = FileResponse(f)
    response["Content-Type"] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="Template.xls"'
    return response


def get_data(obj_list, page):
    paginator = Paginator(obj_list, 10)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except InvalidPage:
        pass
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    return data


def programme_index(request, p_id):
    prog = Programme.objects.filter(id=p_id)
    if len(prog) != 0:
        return render(request, 'oj/programme_index.html', {"programme": prog[0]})
    else:
        return HttpResponse(status=404)


def choice_index(request, c_id):
    choice = Choice.objects.filter(id=c_id)
    if len(choice) != 0:
        return render(request, 'oj/choice_index.html', {"choice": choice[0]})
    else:
        return HttpResponse(status=404)


@require_http_methods(['POST'])
def programme_commit(request, p_id):
    data = json.loads(request.body)
    code = data["code"]
    account = request.session.get("account")
    # commit_dir = os.path.join(RESOURCES_DIR, 'programme', 'commit', str(p_id), str(account))
    # make_dir(commit_dir)
    # c_src = os.path.join(commit_dir, str(time.time()).replace('.', '') + '.c')
    # write_str_file(code, c_src)
    # times = len(
    #     CommitCodeRecord.objects.filter(account=account, problem_id=p_id)
    # ) + 1
    # record = CommitCodeRecord(
    #     problem_id=p_id,
    #     commit_times=times,
    #     account=str(account),
    #     identity='2',
    #     src_content=code,
    #     src_saved_path=c_src
    # )
    # record.save()
    # judger = JudgerUtil(record)
    # judger.judge()
    async_task(
        'apps.oj.tasks.programme_commit',
        account,
        p_id,
        code
    )
    return JsonResponse({"msg": "done"})


def programme_result(request, p_id):
    return render(request, 'oj/programme_result.html')


def choice_commit(request, c_id):
    return HttpResponse("not done")


def check_commit(request):
    pass


def save_tc_file(file_data, tc_dir):
    saved_path = os.path.join(
        RESOURCES_DIR,
        'programme',
        str(time.time()).replace('.', '') + '.zip'
    )
    write_file(file_data, saved_path)
    make_dir(tc_dir)
    unzip_file(saved_path, tc_dir)
