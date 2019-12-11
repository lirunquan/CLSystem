from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.http import require_http_methods
from .models import Teacher, Student
from utils.manager import VerificationCodeGenerator
# Create your views here.

def index(request):
    if request.session.get('is_login') and\
            request.session.get('account'):
        account = request.session.get('account')
        identity = request.session.get('identity')
        if identity == '1':
            user = Teacher.objects.filter(account=account)
        elif identity == '2':
            user = Student.objects.filter(account=account)
        else:
            return HttpResponse(status=400, content='wrong identity')
        if len(user) == 1:
            if user[0].is_login:
                return render(request, 'user/index.html',
                              {"user": user[0]})
            else:
                return redirect('/user/login')
        else:
            return HttpResponse(status=500)
    else:
        return redirect('/user/login')


def login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    elif request.method == 'POST':
        u_account = request.POST.get('account')
        u_password = request.POST.get('password')
        u_identity = request.POST.get('identity')
        u_code = request.POST.get('verify_code')
        if u_code.upper() != request.session.get('verify_code').upper():
            msg = 'wrong verification code'
            return render(request, 'user/login.html', {'message': msg})
        if u_identity == '1':
            user = Teacher.objects.filter(account=u_account)
        elif u_identity == '2':
            user = Student.objects.filter(account=u_account)
        else:
            return HttpResponse(status=500)
        if len(user) == 1:
            if user[0].password == u_password:
                user[0].is_login = True
                user[0].save()
                request.session['account'] = user[0].account
                request.session['identity'] = user[0].identity
                request.session['is_login'] = True
                return redirect('/user/index')
            else:
                msg = 'wrong password'
                return render(request, 'user/login.html', {'message': msg})
        elif len(user) == 0:
            msg = '\'{}\' does not exist'.format(u_account)
            return render(request, 'user/login.html', {'message': msg})
    else:
        return HttpResponse(status=405)

def get_verify_code(request):
    generator = VerificationCodeGenerator()
    verify_code, verify_img = generator.get_code_image()
    request.session['verify_code'] = verify_code
    return HttpResponse(verify_img)

@require_http_methods(["GET"])
def logout(request):
    return redirect('/user/login')


@require_http_methods(["POST"])
def change_password(request):
    pass
