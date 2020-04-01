from django.urls import path
from . import views


urlpatterns = [
    path('index', views.index, name='index'),
    path('mark', views.mark),
    path('<int:m_id>/detail', views.detail, name='detail'),
    path('create', views.create, name='create'),
    path('<int:m_id>/modify', views.modify, name='modify'),
    path('<int:m_id>/commit', views.commit, name='commit'),
    path('<int:m_id>/get_commit', views.get_commit, name='download'),
    path('check/<int:m_id>', views.check_commit, name='check'),
]
