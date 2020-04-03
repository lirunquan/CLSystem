from django.db import models


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

    class Meta:
        abstract = True


class Teacher(User):
    pass


class Student(User):
    class_in = models.ForeignKey(StudentClass, default=1, on_delete=models.CASCADE)
