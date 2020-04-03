# Generated by Django 2.2 on 2020-04-02 20:29

import apps.mission.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publisher', models.CharField(default='', max_length=256)),
                ('title', models.CharField(default='', max_length=256)),
                ('content', models.TextField(default='')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('start_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_at', models.DateTimeField(default=apps.mission.models.end_time)),
                ('to_class', models.CharField(default='', max_length=255)),
            ],
        ),
    ]
