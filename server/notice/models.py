from django.db import models
from django_mysql.models import JSONField
import datetime
# Create your models here.


def announce_time():
    td = datetime.date.today()
    return td + datetime.timedelta(days=1)


def appendix():
    return [
        {"stuffix": "", "filename": "", "saved_path": ""}
    ]


class Appendix(models.Model):
    file_list = JSONField(default=appendix)


class Notice(models.Model):
    publisher = models.CharField(default='', max_length=256)
    title = models.CharField(max_length=256, default='')
    content = models.TextField(default='')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    announce_at = models.DateTimeField(default=announce_time)
    email_alert = models.BooleanField(default=False)
    with_appendix = models.BooleanField(default=False)
    appendix = models.OneToOneField(Appendix, on_delete=models.CASCADE)
