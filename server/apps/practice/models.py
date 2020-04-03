from django.db import models
from django_mysql.models import JSONField
# Create your models here.


PROBLEM_TYPE = (
    ("0", "None"),
    ("1", "Programme"),
    ("2", "Choice"),
)


def choice_options():
    return [
        {"sign": "A", "content": ""},
        {"sign": "B", "content": ""},
        {"sign": "C", "content": ""},
        {"sign": "D", "content": ""}
    ]


class Problem(models.Model):
    title = models.CharField(max_length=256, default='')
    detail = models.TextField(default='')

    class Meta:
        abstract = True


class Programme(Problem):
    input_desc = models.TextField(default='', blank=True)
    output_desc = models.TextField(default='', blank=True)
    input_demo = models.TextField(default='', blank=True)
    output_demo = models.TextField(default='', blank=True)
    time_limit = models.IntegerField(default=1000)  # ms
    memory_limit = models.IntegerField(default=256)  # MB
    testcase_count = models.IntegerField(default=0)
    testcase_dir = models.CharField(default='', max_length=256)


class Choice(Problem):
    multichoice = models.BooleanField(default=False)
    options = JSONField(default=choice_options)
    reference = models.CharField(default='', max_length=10)
