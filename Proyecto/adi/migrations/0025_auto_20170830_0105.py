# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-30 01:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adi', '0024_auto_20170829_2312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curso',
            name='alumno',
        ),
        migrations.AddField(
            model_name='alumno',
            name='curso',
            field=models.ForeignKey(default=543, on_delete=django.db.models.deletion.CASCADE, to='adi.Curso'),
            preserve_default=False,
        ),
    ]
