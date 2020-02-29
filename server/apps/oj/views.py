from django.shortcuts import render, redirect, HttpResponse
from django.http import FileResponse
from django.views.decorators.http import require_http_methods
from django_q.tasks import async_task
from .models import Programme, Choice
from apps.user.views import check_is_login
from server.settings import RESOURCES_DIR
import json
import os
import time
# Create your views here.


def problems_list(request):
    is_login, user = check_is_login(request)
    if is_login == 0:
        return redirect("/user/login")
    if request.method == 'GET':
        if request.GET.get('p_page'):
            p_page = int(request.GET.get('p_page'))
        else:
            p_page = 1
        if request.GET.get('c_page'):
            c_page = int(request.GET.get('c_page'))
        else:
            c_page = 1
        prog_all = Programme.objects.all()
        choice_all = Choice.objects.all()
        prog_data = get_data(prog_all, p_page)
        choice_data = get_data(choice_all, c_page)
        return render(request,
                      'oj/problems_list.html',
                      {"user": user, "p_data": prog_data, "c_data": choice_data})


def add_programme(request):
    if request.method == 'GET':
        return render(request, 'oj/programme_create.html')
    if request.method == 'POST':
        return HttpResponse(status=200)


def add_choice(request):
    return render(request, "oj/choice_create.html")


@require_http_methods(['POST'])
def add_choice_single(request):
    data_dic = json.loads(request.body)
    async_task('tasks.add_choice',
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
    data = []
    for obj in obj_list[(page - 1) * 10: page * 10]:
        data.append({"id": obj.id, "title": obj.title})
    return data
