# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('problems_list', views.problems_list, name='list'),
    path('check_commit', views.check_commit, name='check'),
    path('choice/create', views.add_choice, name='create_choice'),
    path('choice/create/single', views.add_choice_single, name='create_choice_single'),
    path('choice/create/batch', views.add_choice_batch, name='create_choice_batch'),
    path('choice/template_download', views.download_template, name='download'),
    path('programme/create', views.add_programme, name='create_programme'),
    path('programme/<int:p_id>/index', views.programme_index, name='prog_index'),
    path('programme/<int:p_id>/commit', views.programme_commit, name='prog_commit'),
    path('programme/<int:p_id>/result', views.programme_result, name='prog_result'),
    path('programme/<int:p_id>/get_testcase', views.get_tc_zip, name='testcase'),
    path('programme/<int:p_id>/modify', views.programme_modify, name='prog_modify'),
    path('choice/<int:c_id>/index', views.choice_index, name='choice_index'),
    path('choice/<int:c_id>/commit', views.choice_commit, name='choice_commit'),
    path('choice/<int:c_id>/modify', views.choice_modify, name='choice_modify'),
]
