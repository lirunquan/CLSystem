from django.urls import path
from . import views


urlpatterns = [
    path('online_run', views.online_run),
    path('run', views.run),
]
