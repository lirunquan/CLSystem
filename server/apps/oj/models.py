from django.db import models
from django_mysql.models import JSONField
# Create your models here.


PROBLEM_TYPE = (
    ("0", "None"),
    ("1", "Programme"),
    ("2", "Choice"),
    ("3", "Completion"),
)


def choice_options():
    return {
        "A": "",
        "B": "",
        "C": "",
        "D": ""
    }


def completion_answers():
    return {
        "1": ""
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
    cpu_time_limit = models.IntegerField(default=1000)
    memory_limit = models.IntegerField(default=256)
    testcase_num = models.IntegerField(default=0)
    testcase_path = models.CharField(default='', max_length=256)
    requirements = JSONField()
    ext = models.TextField(default='')


class Choice(Problem):
    problem_type = models.CharField(choices=PROBLEM_TYPE, default='2', max_length=2, editable=False)
    multiselect = models.BooleanField(default=False)
    options = JSONField(default=choice_options)
    answer = models.CharField(default='', max_length=10)


class Completion(Problem):
    problem_type = models.CharField(choices=PROBLEM_TYPE, default='3', max_length=2, editable=False)
    blank_num = models.IntegerField(default=1)
    answers = JSONField(default=completion_answers)
