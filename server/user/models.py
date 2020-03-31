from django.db import models


# Create your models here.
USER_IDENTITY = (
    ('1', 'Teacher'),
    ('2', 'Student'),
)


class StudentClass(models.Model):
    year = models.IntegerField(default=2020)
    major = models.CharField(max_length=256, default='')
    number = models.IntegerField(default=1)
    full_name = models.CharField(default='', max_length=255, unique=True)


class User(models.Model):
    account = models.CharField(max_length=20, primary_key=True, null=False, blank=False)
    password = models.CharField(max_length=256, null=False, blank=False)
    email = models.EmailField(default='', blank=True)
    real_name = models.CharField(max_length=50)
    identity = models.CharField()

    class Meta:
        abstract = True


class Teacher(User):
    identity = models.CharField(max_length=2, choices=USER_IDENTITY, default='1')


class Student(User):
    identity = models.CharField(max_length=2, choices=USER_IDENTITY, default='2')
    class_in = models.ForeignKey(StudentClass, default=1, on_delete=models.CASCADE)
