# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 05:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='board',
            old_name='name',
            new_name='slug',
        ),
    ]
