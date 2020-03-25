"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.static import serve
from .settings import MEDIA_ROOT
import notice

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('practice/', include('practice.urls')),
    path('courseware/', include('courseware.urls')),
    path('mission/', include('mission.urls')),
    path('notice/', include('notice.urls')),
    path('comment/', include('comment.urls')),
    path('tool/', include('tool.urls')),
    url(r'^resources/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^$', notice.views.index),
]
