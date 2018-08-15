# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-15 08:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmString',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=256)),
                ('c_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-c_time'],
                'verbose_name_plural': '确认码',
                'verbose_name': '确认码',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='has_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='confirmstring',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='login.User'),
        ),
    ]
