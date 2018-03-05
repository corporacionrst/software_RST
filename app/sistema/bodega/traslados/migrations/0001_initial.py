# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-24 04:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
        ('producto', '0001_initial'),
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DOCUMENTO_A_CANCELAR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=4, default=0, max_digits=300)),
                ('emite_cobro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emite_pago', to='tienda.EMPRESA')),
            ],
        ),
        migrations.CreateModel(
            name='MERCADERIA_A_CANCELAR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NO_TRASLADO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(default=1)),
                ('total', models.DecimalField(decimal_places=4, default=0, max_digits=500)),
                ('a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recibe_traslado', to='tienda.EMPRESA')),
                ('de', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='envia_traslado', to='tienda.EMPRESA')),
            ],
        ),
        migrations.CreateModel(
            name='TRASLADO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(null=True)),
                ('numero', models.IntegerField(default=1)),
                ('cantidad', models.IntegerField(default=0)),
                ('venta', models.DecimalField(decimal_places=4, default=0, max_digits=300)),
                ('no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traslados.NO_TRASLADO')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.PRODUCTO')),
            ],
        ),
        migrations.CreateModel(
            name='TRASLADO_AUTORIZADO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indice', models.IntegerField(default=0)),
                ('autorizada', models.BooleanField(default=False)),
                ('recibe', models.CharField(default='', max_length=200)),
                ('autoriza', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='traslado_autoriza', to='usuarios.Perfil')),
                ('no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traslados.NO_TRASLADO')),
                ('solicita', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='traslado_solicita', to='usuarios.Perfil')),
            ],
        ),
        migrations.AddField(
            model_name='mercaderia_a_cancelar',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traslados.TRASLADO'),
        ),
        migrations.AddField(
            model_name='documento_a_cancelar',
            name='lista_a_cancelar',
            field=models.ManyToManyField(to='traslados.MERCADERIA_A_CANCELAR'),
        ),
        migrations.AddField(
            model_name='documento_a_cancelar',
            name='recibe_cobro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recibe_pago', to='tienda.EMPRESA'),
        ),
    ]