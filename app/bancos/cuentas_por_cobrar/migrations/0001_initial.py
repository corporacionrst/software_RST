# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-24 04:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
        ('historial', '0001_initial'),
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DOCUMENTO_POR_COBRAR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_limite', models.DateField()),
                ('pendiente', models.DecimalField(decimal_places=4, default=0, max_digits=300)),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='historial.HISTORIAL')),
            ],
        ),
        migrations.CreateModel(
            name='DOCUMENTO_RECIBOS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_limite', models.DateField()),
                ('correlativo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LISTA_RECIBOS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correlativo', models.IntegerField(default=1)),
                ('caja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Perfil')),
                ('tienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.EMPRESA')),
            ],
        ),
        migrations.AddField(
            model_name='documento_recibos',
            name='Recibo_tienda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cuentas_por_cobrar.LISTA_RECIBOS'),
        ),
    ]
