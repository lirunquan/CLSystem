from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.http import require_http_methods
from .models import Teacher, Student



# Create your views here.

def index(request):

    account = request.GET.get('account')
    identity = request.GET.get('identity')
    # if request.session.get('is_login') and\
    #         request.session.get('account') == account:
    user = ''
    if identity == '1':
        user = Teacher.objects.filter(account=account)
    elif identity == '2':
        user = Student.objects.filter(account=account)
    else:
        return HttpResponse(status=400, content='wrong identity')
    if len(user) == 1:
        if user[0].is_login:
            return render(request, 'user/index.html',
                          {"account": account,
                           "email": user[0].email,
                           "real_name": user[0].real_name})
        else:
            return redirect('/user/login')
    # else:
    #     return redirect('/user/login')


def login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')




@require_http_methods(["GET"])
def logout(request):
    return redirect('/user/login')


@require_http_methods(["POST"])
def changepassword(request):
    pass
