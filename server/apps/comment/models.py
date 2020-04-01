from django.db import models

# Create your models here.


class Comment(models.Model):
    writer = models.CharField(max_length=256, default='')
    content = models.TextField(default='')
    leave_time = models.DateTimeField(auto_now_add=True)
