# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-27 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historial', '0004_auto_20180227_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record_de_ventas',
            name='facturas',
            field=models.ManyToManyField(blank=True, related_name='documentos', to='historial.HISTORIAL'),
        ),
    ]