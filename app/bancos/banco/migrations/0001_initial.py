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
            name='BANCO',
            fields=[
                ('nombre', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='CUENTA_BANCARIA',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('numero_de_cuenta', models.CharField(max_length=100)),
                ('capital', models.DecimalField(decimal_places=2, default=0, max_digits=300)),
                ('administra', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.Perfil')),
                ('banco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banco.BANCO')),
                ('tienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.EMPRESA')),
            ],
        ),
    ]
