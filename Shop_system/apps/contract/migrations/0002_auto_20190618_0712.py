# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-18 07:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='contract_rent',
            field=models.IntegerField(verbose_name='月租金'),
        ),
    ]
