from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('chapter/create', views.chapter_create, name='chapter_create'),
    path('chapter/<int:c_id>/index', views.chapter_index, name='chapter_index'),
    path('chapter/<int:c_id>/modify', views.chapter_modify, name='chapter_modify'),
    path('notice/create', views.notice_create, name='notice_create'),
    path('notice/index', views.notice_index, name='notice_index'),
    path('notice/<int:n_id>/detail', views.notice_detail, name='notice_detail'),
    path('notice/<int:n_id>/modify', views.notice_modify, name='notice_modify'),
    path('mission/create', views.mission_create, name='mission_create'),
    path('mission/<int:n_id>/index', views.mission_index, name='mission_index'),
    path('mission/<int:n_id>/modify', views.mission_modify, name='mission_modify'),
    path('mission/<int:n_id>/commit', views.mission_commit, name='mission_commit'),
]
