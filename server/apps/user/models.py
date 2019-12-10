from django.db import models


# Create your models here.
USER_IDENTITY = (
    ('1', 'Teacher'),
    ('2', 'Student'),
)


class User(models.Model):
    account = models.CharField(max_length=20, primary_key=True, null=False, blank=False)
    password = models.CharField(max_length=256, null=False, blank=False)
    email = models.EmailField(default='')
    real_name = models.CharField(max_length=50)
    is_login = models.BooleanField(default=False)
    identity = models.CharField()

    class Meta:
        abstract = True


class Teacher(User):
    identity = models.CharField(max_length=2, choices=USER_IDENTITY, default='1')


class Student(User):
    identity = models.CharField(max_length=2, choices=USER_IDENTITY, default='2')
