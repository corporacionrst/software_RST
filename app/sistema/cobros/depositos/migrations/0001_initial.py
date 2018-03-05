# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-24 04:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('banco', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DEPOSITOS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateField(auto_now_add=True)),
                ('documento', models.CharField(default='', max_length=300)),
                ('monto', models.DecimalField(decimal_places=2, default=0, max_digits=300)),
                ('visto', models.BooleanField(default=False)),
                ('confirmar', models.BooleanField(default=False)),
                ('cuenta_acreditada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='para', to='banco.CUENTA_BANCARIA')),
                ('cuenta_debitada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='de', to='banco.CUENTA_BANCARIA')),
            ],
        ),
    ]