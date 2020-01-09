from django.db import models

# Create your models here.
class Chapter(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(default='', max_length=256)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('id',)

class Section(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(default='', max_length=256)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('id',)