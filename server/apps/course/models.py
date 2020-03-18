from django.db import models
from django.utils import timezone
from django_mysql.models import JSONField
import datetime
# Create your models here.


COURSEWARE = (
    ('1', 'PowerPoint'),
    ('2', 'Video'),
    ('3', 'PDF'),
)


class Chapter(models.Model):
    chapter_num = models.IntegerField(default=0, unique=True)
    title = models.CharField(default='', max_length=256)
    courseware_path = models.CharField(default='', max_length=256)
    courseware_type = models.CharField(max_length=2, choices=COURSEWARE, default='1')

    class Meta:
        ordering = ('id',)


def announce_time():
    td = datetime.date.today()
    return datetime.datetime(td.year, td.month, td.day + 1, 7, 0, 0)


def appendix():
    return [
        {"stuffix": "", "saved_path": ""}
    ]


class Appendix(models.Model):
    file_list = JSONField(default=appendix)


class Notice(models.Model):
    title = models.CharField(max_length=256, default='')
    content = models.TextField(default='')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    announce_at = models.DateTimeField(default=announce_time)
    email_alert = models.BooleanField(default=False)
    with_appendix = models.BooleanField(default=False)
    appendix = models.OneToOneField(Appendix, on_delete=models.CASCADE)


def end_time():
    td = datetime.date.today()
    return datetime.datetime(td.year, td.month, td.day + 7, 18, 0, 0)


class Mission(models.Model):
    title = models.CharField(max_length=256, default='')
    content = models.TextField(default='')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    start_at = models.DateTimeField(default=timezone.now)
    end_at = models.DateTimeField(default=end_time)
