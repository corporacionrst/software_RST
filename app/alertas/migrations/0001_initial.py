# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-24 04:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ALERTA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.IntegerField(default=0)),
                ('mensaje', models.CharField(default='', max_length=300)),
                ('sub_mensaje', models.CharField(default='', max_length=300)),
                ('ruta', models.CharField(default='', max_length=2000)),
                ('visto', models.BooleanField(default=False)),
                ('puesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.PUESTO')),
                ('requiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Perfil')),
                ('tienda', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tienda_solicitud', to='tienda.EMPRESA')),
            ],
        ),
    ]
