from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('<int:n_id>/detail', views.detail, name='detail'),
    path('create', views.create, name='create'),
    path('<int:n_id>/modify', views.modify, name='modify'),
    path('<int:n_id>/appendix', views.get_appendix, name='appendix'),
]
