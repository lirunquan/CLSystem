from django.shortcuts import render, redirect, HttpResponse
from django.http import FileResponse
from django.views.decorators.http import require_http_methods
from .models import Programme, Choice
from apps.user.views import check_is_login
from utils.FileUtil import handle_batch_choice_excel
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
    pass


def add_choice(request):
    return render(request, "oj/choice_create.html")


@require_http_methods(['POST'])
def add_choice_single(request):
    data_dic = json.loads(request.body)
    choice = Choice(
        title=data_dic["title"],
        detail=data_dic["detail"],
        options=data_dic["options"],
        multichoice=data_dic["multichoice"],
        reference=data_dic["reference"]
    )
    choice.save()
    return HttpResponse(status=200)


@require_http_methods(['POST'])
def add_choice_batch(request):
    execel_file = request.FILES.get("excel")
    filename = "upload_" + str(time.time()).replace('.', '') + '.xls'
    saved_path = os.path.join(RESOURCES_DIR, 'choices', filename)
    with open(saved_path, 'wb') as f:
        for i in execel_file.chunks():
            f.write(i)
    data_list = handle_batch_choice_excel(saved_path)
    print(data_list)
    for c in data_list:
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
    data = []
    for obj in obj_list[(page - 1) * 10: page * 10]:
        data.append({"id": obj.id, "title": obj.title})
    return data
