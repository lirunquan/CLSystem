from django.db import models
from django_mysql.models import JSONField
from apps.user.models import USER_IDENTITY
from apps.oj.models import PROBLEM_TYPE
# Create your models here.


class Record(models.Model):
    account = models.CharField(max_length=50, default='')
    identity = models.CharField(choices=USER_IDENTITY, default='2', max_length=2)
    time = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    ext = models.TextField(default='', blank=True)
    operation = models.CharField()

    class Meta:
        abstract = True


# record while user logins
class LoginRecord(Record):
    operation = models.CharField(default='login', max_length=20, editable=False)


# record while user certificates email
class EmailCertificationRecord(Record):
    operation = models.CharField(default='certificate email', max_length=50, editable=False)
    email = models.TextField(default='')


# record while user changes password
class ChangePasswordRecord(Record):
    operation = models.CharField(default='change password', max_length=50, editable=False)
    old_password = models.CharField(max_length=256, default='')
    new_password = models.CharField(max_length=256, default='')


class EmailSentRecord(Record):
    operation = models.CharField(default='send email', max_length=20, editable=False)
    email_type = models.CharField(max_length=256)
    recipients = models.TextField(default='')


class CertificationSentRecord(EmailSentRecord):
    active_code = models.CharField(max_length=50, default='')
    token = models.CharField(max_length=50, default='')


class VerifyCodeSentRecord(EmailSentRecord):
    code = models.CharField(max_length=20, default='')


class CommitRecord(Record):
    operation = models.CharField(default='commit', max_length=20, editable=False)
    problem_id = models.IntegerField(default=0)
    problem_type = models.CharField(choices=PROBLEM_TYPE, default='0', max_length=2)
    commit_times = models.IntegerField(default=0)
    ext = models.TextField(default='')

    class Meta:
        abstract = True


class CommitCodeRecord(CommitRecord):
    problem_type = models.CharField(choices=PROBLEM_TYPE, default='1', max_length=2)
    src_content = models.TextField(default='')
    src_saved_path = models.CharField(max_length=256)


class CommitChoiceRecord(CommitRecord):
    problem_type = models.CharField(choices=PROBLEM_TYPE, default='2', max_length=2)
    correct = models.BooleanField(default=False)
    answer = models.CharField(default='', max_length=20)


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
