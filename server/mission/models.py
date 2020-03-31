from django.db import models
from django.utils import timezone
import datetime
# Create your models here.


def end_time():
    td = datetime.date.today()
    nw = td + datetime.timedelta(days=7)
    return datetime.datetime(
        nw.year, nw.month, nw.day, 7, 0, 0
    )


class Mission(models.Model):
    publisher = models.CharField(default='', max_length=256)
    title = models.CharField(max_length=256, default='')
    content = models.TextField(default='')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    start_at = models.DateTimeField(default=timezone.now)
    end_at = models.DateTimeField(default=end_time)
    to_class = models.CharField(max_length=255, default='')
