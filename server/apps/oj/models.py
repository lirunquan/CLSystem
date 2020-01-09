from django.db import models
from django_mysql.models import JSONField
# Create your models here.


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
    input_demo = models.TextField(default='', blank=True)
    output_demo = models.TextField(default='', blank=True)
    time_claim = models.IntegerField(default=1000)
    memory_claim = models.IntegerField(default=256)
    test_case_in = models.CharField(max_length=256, default='', blank=True)
    test_case_out = models.CharField(max_length=256, default='', blank=True)
    test_case_cpp = models.CharField(max_length=256, default='', blank=True)
    requirements = JSONField()
    ext = models.TextField(default='')

class Choice(Problem):
    multiselect = models.BooleanField(default=False)
    options = JSONField(default=choice_options)
    answer = models.CharField(default='', max_length=10)

class Completion(Problem):
    blank_num = models.IntegerField(default=1)
    answers = JSONField(default=completion_answers)

