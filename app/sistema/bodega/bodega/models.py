# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ....productos.inventario.historial.models import LISTA_PRODUCTO
# Create your models here.
class COLA_DESPACHO(models.Model):
	producto = models.ForeignKey(LISTA_PRODUCTO)
