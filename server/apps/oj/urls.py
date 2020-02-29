# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('problems_list', views.problems_list, name='list'),
    path('choice/create', views.add_choice, name='create_choice'),
    path('choice/create/single', views.add_choice_single, name='create_choice_single'),
    path('choice/create/batch', views.add_choice_batch, name='create_choice_batch'),
    path('choice/template_download', views.download_template, name='download'),
    path('programme/create', views.add_programme, name='create_programme'),
]
