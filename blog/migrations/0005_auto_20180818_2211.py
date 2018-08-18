# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-18 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_remove_comment_parent_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-m_time'], 'verbose_name': '博客', 'verbose_name_plural': '博客'},
        ),
        migrations.AddField(
            model_name='blog',
            name='m_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
