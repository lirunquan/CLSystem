from django.shortcuts import render

from .models import Programme, Choice
# Create your views here.


def problems_list(request):
    if request.method == 'GET':
        p_page = 1
        c_page = 1
        if request.GET.get('p_page'):
            p_page = int(request.GET.get('p_page'))
        if request.GET.get('c_page'):
            c_page = int(request.GET.get('c_page'))
        prog_all = Programme.objects.all()
        choice_all = Choice.objects.all()
        prog_data = get_data(prog_all, p_page)
        choice_data = get_data(choice_all, c_page)
        return render(request,
                      'oj/problems_list.html',
                      {"p_data": prog_data, "c_data": choice_data})


def add_programme(request):
    pass


def add_choice(request):
    pass


def add_choice_single(request):
    pass


def add_choice_batch(request):
    pass


def get_data(obj_list, page):
    data = []
    for obj in obj_list[(page - 1) * 10: page * 10]:
        data.append({"id": obj.id, "title": obj.title})
    return data
