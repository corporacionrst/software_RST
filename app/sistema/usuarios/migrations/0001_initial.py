# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-24 04:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tienda', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DOCUMENTO_POR_TIENDA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pagina', models.IntegerField(default=0)),
                ('correlativo', models.IntegerField(default=1)),
                ('tipo_doc', models.CharField(default='V', max_length=1)),
                ('credito', models.BooleanField(default=False)),
                ('total', models.DecimalField(decimal_places=4, default=0, max_digits=300)),
                ('descuento', models.DecimalField(decimal_places=4, default=0, max_digits=300)),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='usuario', max_length=50)),
                ('apellido', models.CharField(default='apellido', max_length=50)),
                ('direccion', models.CharField(default='direccion', max_length=200)),
                ('fecha_nacimiento', models.DateField()),
                ('fecha_ingreso', models.DateField()),
                ('documento4', models.CharField(default='4-a-1', max_length=300)),
                ('multitienda', models.BooleanField(default=False)),
                ('cui', models.CharField(default='', max_length=100)),
                ('ultima_indemnizacion', models.DateField()),
                ('no_igss', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PUESTO',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='USUARIO_TIENDA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actual', models.IntegerField(default=1)),
                ('orden', models.IntegerField(default=1)),
                ('fac_1', models.IntegerField(default=1)),
                ('fac_2', models.IntegerField(default=1)),
                ('fac_3', models.IntegerField(default=1)),
                ('fac_4', models.IntegerField(default=1)),
                ('tienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store', to='tienda.EMPRESA')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='usuarios.Perfil')),
            ],
        ),
        migrations.AddField(
            model_name='perfil',
            name='puesto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.PUESTO'),
        ),
        migrations.AddField(
            model_name='perfil',
            name='tienda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.EMPRESA'),
        ),
        migrations.AddField(
            model_name='perfil',
            name='usuario',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='documento_por_tienda',
            name='ubicado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.USUARIO_TIENDA'),
        ),
    ]
