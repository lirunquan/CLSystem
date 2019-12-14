from django.db import models

# Create your models here.

class Record(models.Model):
    user = models.CharField(max_length=50, default='')
    time = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    ext = models.TextField(default='', blank=True)
    operation = models.CharField()
    class Meta:
        abstract = True

class LoginRecord(Record):
    operation = models.CharField(default='login', max_length=20, editable=False)

class EmailSentRecord(Record):
    operation = models.CharField(default='send email', max_length=20, editable=False)
    email_type = models.CharField(max_length=256)
    recipients = models.TextField(default='')

class CertificationSentRecord(EmailSentRecord):
    active_code = models.CharField(max_length=50, default='')
    token = models.CharField(max_length=50, default='')

class EmailCertificationRecord(Record):
    operation = models.CharField(default='certificate email', max_length=50, editable=False)
    email = models.TextField(default='')

class ChangePasswordRecord(Record):
    operation = models.CharField(default='change password', max_length=50, editable=False)
    new_password = models.CharField(max_length=256)
