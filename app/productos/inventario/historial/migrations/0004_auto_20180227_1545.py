# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-27 15:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historial', '0003_record_de_ventas_tienda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record_de_ventas',
            name='facturas',
            field=models.ManyToManyField(null=True, related_name='documentos', to='historial.HISTORIAL'),
        ),
    ]
