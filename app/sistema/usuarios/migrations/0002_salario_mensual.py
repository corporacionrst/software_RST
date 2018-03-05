# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-25 02:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SALARIO_MENSUAL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_de_pago', models.DateField()),
                ('salario', models.DecimalField(decimal_places=4, max_digits=300)),
                ('comision', models.DecimalField(decimal_places=4, default=0, max_digits=300)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Perfil')),
            ],
        ),
    ]
