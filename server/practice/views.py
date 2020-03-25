from django.shortcuts import render, redirect, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import FileResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Programme, Choice
from record.models import CommitCodeRecord, CommitChoiceRecord
from server.settings import RESOURCES_DIR
from utils.FileUtil import *
from utils.JudgerUtil import JudgerUtil
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
            'practice/problems_list.html',
            {
                "p_data": prog_data,
                "p_len": len(prog_all),
                "c_data": choice_data,
                "c_len": len(choice_all)
            })


def add_programme(request):
    if request.method == 'GET':
        return render(request, 'practice/programme_create.html')
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
        return redirect('/practice/problems_list')


def add_choice(request):
    return render(request, "practice/choice_create.html")


@require_http_methods(['POST'])
def add_choice_single(request):
    data_dic = json.loads(request.body)
    if data_dic["title"] == "":
        return JsonResponse({"msg": "failed"})
    if data_dic["detail"] == "":
        return JsonResponse({"msg": "failed"})
    for o in data_dic["options"]:
        if o["content"] == "":
            return JsonResponse({"msg": "failed"})
    if data_dic["reference"] == "":
        return JsonResponse({"msg": "failed"})
    c = Choice(
        title=data_dic["title"],
        detail=data_dic["detail"],
        options=data_dic["options"],
        multichoice=data_dic["multichoice"],
        reference=data_dic["reference"]
    )
    c.save()
    return JsonResponse({"msg": "done"})


@require_http_methods(['POST'])
def add_choice_batch(request):
    execel_file = request.FILES.get("excel")
    filename = "upload_" + str(time.time()).replace('.', '') + '.xls'
    saved_path = os.path.join(RESOURCES_DIR, 'choices', filename)
    write_file(execel_file, saved_path)
    choices_list = handle_choice_excel(saved_path)
    for c in choices_list:
        options = [
            {"sign": "A", "content": c["A"]},
            {"sign": "B", "content": c["B"]},
            {"sign": "C", "content": c["C"]},
            {"sign": "D", "content": c["D"]}
        ]
        choice = Choice(
            title=c["title"],
            detail=c["detail"],
            options=options,
            multichoice=c["multichoice"] == 'Y',
            reference=c["reference"]
        )
        choice.save()
    remove_file(saved_path)
    return redirect("/practice/problems_list")


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
        return render(request, 'practice/programme_index.html', {"programme": prog[0]})
    else:
        return HttpResponse(status=404)


def choice_index(request, c_id):
    choice = Choice.objects.filter(id=c_id)
    if len(choice) != 0:
        return render(
            request,
            'practice/choice_index.html',
            {"choice": choice[0], "count": len(choice[0].options)}
        )
    else:
        return HttpResponse(status=404)


@require_http_methods(['POST'])
def programme_commit(request, p_id):
    data = json.loads(request.body)
    code = data["code"]
    account = request.session.get("account")
    commit_dir = os.path.join(RESOURCES_DIR, 'programme', 'commit', str(p_id), str(account))
    make_dir(commit_dir)
    c_src = os.path.join(commit_dir, str(time.time()).replace('.', '') + '.c')
    write_str_file(code, c_src)
    times = len(
        CommitCodeRecord.objects.filter(account=account, problem_id=p_id)
    ) + 1
    record = CommitCodeRecord(
        problem_id=p_id,
        commit_times=times,
        account=str(account),
        identity='2',
        src_content=code,
        src_saved_path=c_src
    )
    record.save()
    judger = JudgerUtil(record)
    judger.judge()
    return JsonResponse({"msg": "done"})


@require_http_methods(['GET'])
def programme_result(request, p_id):
    account = request.session.get("account")
    commits = CommitCodeRecord.objects.order_by('-time').filter(account=account, problem_id=p_id)
    title = Programme.objects.get(id=p_id).title
    page = int(request.GET.get("page")) if request.GET.get("page") else 1
    rsts = []
    for c in commits:
        compiled = c.compilesrcrecord
        judged = compiled.judgerecord
        r = get_result(compiled, judged)
        code = c.src_content
        t = c.time.strftime('%Y/%m/%d %H:%M:%S')
        rsts.append(
            {
                "id": c.id,
                "account": account,
                "result": r,
                "time": t,
                "code": code,
                "title": title
            }
        )
    rst_data = get_data(rsts, page)
    return render(
        request,
        'practice/programme_result.html',
        {"results": rst_data, "count": len(rsts)}
    )


def choice_commit(request, c_id):
    data = json.loads(request.body)
    answer = data["answer"]
    choice = Choice.objects.get(id=c_id)
    reference = choice.reference
    record = CommitChoiceRecord(
        account=request.session.get("account"),
        problem_id=c_id,
        answer=answer,
        correct=answer == reference
    )
    record.save()
    ret = {"correct": answer == reference}
    return JsonResponse(ret)


def check_commit(request):
    page = int(request.GET.get("page")) if request.GET.get("page") else 1
    commits = CommitCodeRecord.objects.order_by('-time')
    if request.GET.get("p_id"):
        commits = commits.filter(problem_id=int(request.GET.get("p_id")))
    if request.GET.get("account"):
        commits = commits.filter(account=str(request.GET.get("account")))
    data_list = []
    for c in commits:
        account = c.account
        title = Programme.objects.get(id=c.problem_id).title
        t = c.time.strftime('%Y-%m-%d %H:%M:%S')
        code = c.src_content
        compiled = c.compilesrcrecord
        judged = compiled.judgerecord
        r = get_result(compiled, judged)
        data_list.append(
            {
                "id": c.id,
                "account": account,
                "result": r,
                "time": t,
                "code": code,
                "title": title
            }
        )
    new_list = data_list
    if request.GET.get("result"):
        new_list = [
            d for d in data_list if d["result"] == request.GET.get("result")
        ]
    data = get_data(new_list, page)
    return render(
        request,
        'practice/check_commit.html',
        {"results": data, "status": request.GET.get("result")}
    )


@require_http_methods(['POST'])
def choice_modify(request, c_id):
    data = json.loads(request.body)
    choice = Choice.objects.filter(id=c_id)
    if data.get("operation") == "remove":
        if len(choice) == 1:
            choice.delete()
            return JsonResponse({"msg": "done"})
    if data.get("operation") == "change":
        if data["title"] == "":
            return JsonResponse({"msg": "empty"})
        if data["detail"] == "":
            return JsonResponse({"msg": "empty"})
        for o in data["options"]:
            if o["content"] == "":
                return JsonResponse({"msg": "empty"})
        if data["reference"] == "":
            return JsonResponse({"msg": "empty"})
        ret = 0
        if len(choice) == 1:
            ret = choice.update(
                title=data.get("title"),
                detail=data.get("detail"),
                options=data.get("options"),
                multichoice=data.get("multichoice"),
                reference=data.get("reference")
            )
        if ret == 1:
            return JsonResponse({"msg": "done"})
    return JsonResponse({"msg": "failed"})


def programme_modify(request, p_id):
    programme = Programme.objects.filter(id=p_id)
    if request.POST.get("operation") == "remove":
        if len(programme) == 1:
            make_dir(programme.testcase_dir)
            os.rmdir(programme.testcase_dir)
            programme.delete()
            return JsonResponse({"msg": "done"})
    file = request.FILES.get("testcase_zip")
    if len(programme) == 1:
        if file:
            save_tc_file(file, programme[0].testcase_dir)
        title = request.POST.get("title")
        detail = request.POST.get("detail")
        input_desc = request.POST.get("input_desc")
        output_desc = request.POST.get("output_desc")
        input_demo = request.POST.get("input_demo")
        output_demo = request.POST.get("output_demo")
        testcase_count = request.POST.get("testcase_count")
        time_limit = request.POST.get("time_limit")
        memory_limit = request.POST.get("memory_limit")
        ret = programme.update(
            title=title,
            detail=detail,
            input_desc=input_desc,
            output_desc=output_desc,
            input_demo=input_demo,
            output_demo=output_demo,
            time_limit=time_limit,
            memory_limit=memory_limit,
            testcase_count=testcase_count,
        )
        if ret == 1:
            return redirect("/practice/programme/" + str(p_id) + "/index")
    return HttpResponse(status=500)


@require_http_methods(["GET"])
def get_tc_zip(request, p_id):
    prog = Programme.objects.filter(id=p_id)
    if len(prog) == 1:
        tc_dir = prog[0].testcase_dir
        z = os.path.join(
            RESOURCES_DIR,
            'programme',
            str(time.time()).replace('.', '') + '.zip'
        )
        make_zip(tc_dir, z)
        f = open(z, 'rb')
        response = FileResponse(f)
        response["Content-Type"] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="testcase.zip"'
        return response
    return HttpResponse(status=404)


def save_tc_file(file_data, tc_dir):
    saved_path = os.path.join(
        RESOURCES_DIR,
        'programme',
        str(time.time()).replace('.', '') + '.zip'
    )
    write_file(file_data, saved_path)
    make_dir(tc_dir)
    unzip_file(saved_path, tc_dir)
    remove_file(saved_path)


def get_result(compile_obj, judge_obj):
    if compile_obj.success:
        result = judge_obj.result
        if isinstance(result, list):
            for r in result:
                if r["error"] == 0:
                    if r["result"] != "ACCEPT":
                        return r["result"]
                else:
                    return r["error"]
            return "ACCEPT"
        if isinstance(result, dict):
            return result.get("result")
    return "COMPILE_ERROR"
