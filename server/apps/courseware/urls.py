from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('index', views.index, name='index'),
    path('<int:c_id>/detail', views.detail, name='detail'),
    path('<int:c_id>/modify', views.modify, name='modify'),
    path('download', views.download),
    url('stream/', views.stream),
]
