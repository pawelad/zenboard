# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 05:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_rename_name_field_to_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name='name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='board',
            name='show_closed_pipeline',
            field=models.BooleanField(default=True, verbose_name="show 'Closed' pipeline"),
        ),
        migrations.AlterField(
            model_name='board',
            name='filter_sign',
            field=models.CharField(blank=True, default='🐙', help_text='Issue description and comments will only be visible if they contain this sign / string. If none provided, everything will be shown.', max_length=16, verbose_name='filter sign'),
        ),
        migrations.AlterField(
            model_name='board',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='slug'),
        ),
    ]
