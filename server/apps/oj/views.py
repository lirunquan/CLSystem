from django.shortcuts import render, redirect, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import FileResponse
from django.views.decorators.http import require_http_methods
from django_q.tasks import async_task
from .models import Programme, Choice
from server.settings import RESOURCES_DIR
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
        return render(request,
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
        async_task("apps.oj.tasks.save_tc_file",
                   testcase_file,
                   tc_dir
                   )
        async_task("apps.oj.tasks.add_programme",
                   title,
                   detail,
                   input_desc,
                   output_desc,
                   input_demo,
                   output_demo,
                   testcase_count,
                   tc_dir,
                   time_limit,
                   memory_limit
                   )
        time.sleep(2)
        return redirect('/oj/problems_list')


def add_choice(request):
    return render(request, "oj/choice_create.html")


@require_http_methods(['POST'])
def add_choice_single(request):
    data_dic = json.loads(request.body)
    async_task('apps.oj.tasks.add_choice',
               data_dic["title"],
               data_dic["detail"],
               data_dic["options"],
               data_dic["multichoice"],
               data_dic["reference"]
               )
    return HttpResponse(status=200)


@require_http_methods(['POST'])
def add_choice_batch(request):
    execel_file = request.FILES.get("excel")
    filename = "upload_" + str(time.time()).replace('.', '') + '.xls'
    saved_path = os.path.join(RESOURCES_DIR, 'choices', filename)
    async_task('tasks.import_choice_from_excel',
               execel_file,
               saved_path
               )
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


def programme_commit(request, p_id):
    return HttpResponse("not done")


def choice_commit(request, c_id):
    return HttpResponse("not done")
