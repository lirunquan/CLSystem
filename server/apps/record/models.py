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


COMMIT_STATUS = (
    ("-1", "Error"),
    ("1", "Accepted"),
    ("2", "Compiling"),
    ("3", "Wait For Judge"),
)


class CommitRecord(Record):
    operation = models.CharField(default='commit', max_length=20, editable=False)
    problem_id = models.IntegerField(default=0)
    problem_type = models.CharField(choices=PROBLEM_TYPE, default='0', max_length=2)
    status = models.CharField(choices=COMMIT_STATUS, max_length=10)
    commit_times = models.IntegerField(default=0)
    ext = models.TextField(default='')

    class Meta:
        abstract = True


class CommitCodeRecord(CommitRecord):
    src_content = models.TextField(default='')
    src_saved_path = models.CharField(max_length=256)


class CommitChoiceRecord(CommitRecord):
    choice = models.CharField(default='', max_length=20)


def completion_answers():
    return {}


class CommitCompletionRecord(CommitRecord):
    answers = JSONField(default=completion_answers)


class CompileSrcRecord(models.Model):
    time = models.DateTimeField(auto_now=True)
    commit_record = models.OneToOneField(CommitCodeRecord, on_delete=models.CASCADE)
    exe_path = models.CharField(default='', max_length=256)
    result = models.TextField(default='')


class JudgeRecord(models.Model):
    time = models.DateTimeField(auto_now=True)
    compile_record = models.OneToOneField(CompileSrcRecord, on_delete=models.CASCADE)
    testcase_number = models.IntegerField(default=0)
    testcase_path = models.CharField(default='', max_length=256)
    result = models.TextField(default='')
