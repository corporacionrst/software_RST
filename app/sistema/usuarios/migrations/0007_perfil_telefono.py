# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-01 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_usuario_tienda_proforma'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='telefono',
            field=models.CharField(default='2208-1414', max_length=10),
        ),
    ]