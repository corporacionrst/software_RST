# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-28 21:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proformas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proforma',
            name='fecha_vencimiento',
            field=models.DateField(),
        ),
    ]
