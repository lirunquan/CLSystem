from django.db import models

# Create your models here.


COURSEWARE = (
    ('0', 'Other'),
    ('1', 'PPT'),
    ('2', 'Video'),
    ('3', 'PDF'),
)


class Courseware(models.Model):
    ordinal = models.IntegerField(default=0, unique=True)
    title = models.CharField(default='', max_length=256)
    file_path = models.CharField(default='', max_length=256)
    file_type = models.CharField(max_length=2, choices=COURSEWARE, default='1')
    show_path = models.CharField(max_length=256, default='')

    class Meta:
        ordering = ('ordinal',)
