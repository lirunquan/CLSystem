# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('getVerificationCode', views.get_verify_code, name='code'),
    path('email/certificate', views.certificate_email, name='certificate'),
    url(r'^email/active/', views.active_email),
    path('email/verifyCode', views.send_verify_code, name='sendVerifyCOde'),
    path('changePassword', views.change_password, name='changePassword'),
    path('forgot', views.forgot_password, name='forgot'),
    url(r'^login/$', views.login),
    path('import', views.import_user, name='importPage'),
    path('import/<int:identity>', views.import_user_save, name='saveUser'),
    path('template/student', views.download_student, name='stuTemp'),
    path('template/teacher', views.download_teacher, name='tecTemp'),
    path('add_class', views.add_class),
]
