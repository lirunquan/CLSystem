from django.db import models
from django_mysql.models import JSONField
# Create your models here.


PROBLEM_TYPE = (
    ("0", "None"),
    ("1", "Programme"),
    ("2", "Choice"),
)


def choice_options():
    return {
        "A": "",
        "B": "",
        "C": "",
        "D": ""
    }


class Problem(models.Model):
    title = models.CharField(max_length=256, default='')
    detail = models.TextField(default='')
    chapter_id = models.IntegerField(default=1)

    class Meta:
        abstract = True


class Programme(Problem):
    problem_type = models.CharField(choices=PROBLEM_TYPE, default='1', max_length=2, editable=False)
    input_desc = models.TextField(default='', blank=True)
    output_desc = models.TextField(default='', blank=True)
    input_demo = models.TextField(default='', blank=True)
    output_demo = models.TextField(default='', blank=True)
    time_limit = models.IntegerField(default=1000)  # ms
    memory_limit = models.IntegerField(default=20000)  # KB
    testcase_count = models.IntegerField(default=0)
    testcase_dir = models.CharField(default='', max_length=256)
    requirements = JSONField()
    ext = models.TextField(default='')


class Choice(Problem):
    problem_type = models.CharField(choices=PROBLEM_TYPE, default='2', max_length=2, editable=False)
    multiselect = models.BooleanField(default=False)
    options = JSONField(default=choice_options)
    reference = models.CharField(default='', max_length=10)
