from django.db import models
from django_mysql.models import JSONField
# Create your models here.


USER_IDENTITY = (
    ('1', 'Teacher'),
    ('2', 'Student')
)


class Record(models.Model):
    account = models.CharField(max_length=50, default='')
    time = models.DateTimeField(auto_now_add=True)
    identity = models.CharField(choices=USER_IDENTITY, default='2', max_length=2)
    success = models.BooleanField(default=True)
    ext = models.TextField(default='', blank=True)

    class Meta:
        abstract = True


class EmailSentRecord(Record):
    email_type = models.CharField(max_length=256)
    recipients = models.TextField(default='')


class CertificationSentRecord(EmailSentRecord):
    active_code = models.CharField(max_length=50, default='')
    token = models.CharField(max_length=50, default='')


class VerifyCodeSentRecord(EmailSentRecord):
    code = models.CharField(max_length=20, default='')


class CommitCodeRecord(Record):
    problem_id = models.IntegerField(default=0)
    commit_times = models.IntegerField(default=0)
    src_content = models.TextField(default='')
    src_saved_path = models.CharField(max_length=256)


class CompileSrcRecord(models.Model):
    time = models.DateTimeField(auto_now=True)
    commit_record = models.OneToOneField(CommitCodeRecord, on_delete=models.CASCADE)
    exe_path = models.CharField(default='', max_length=256)
    ext = models.TextField(default='')
    success = models.BooleanField(default=False)


def judge_result():
    return []


class JudgeRecord(models.Model):
    time = models.DateTimeField(auto_now=True)
    compile_record = models.OneToOneField(CompileSrcRecord, on_delete=models.CASCADE)
    result = JSONField(default=judge_result)


class CommitMissionRecord(models.Model):
    time = models.DateTimeField(auto_now=True)
    account = models.CharField(max_length=50, default='')
    mission_id = models.IntegerField(default=0)
    saved_path = models.CharField(max_length=256, default='')
    grade = models.CharField(max_length=20, default='None')
