# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from ...producto.models import PRODUCTO
from ....sistema.tienda.models import EMPRESA



class INVENTARIO(models.Model):
	tienda= models.ForeignKey(EMPRESA)
	producto = models.ForeignKey(PRODUCTO)
	cantidad = models.IntegerField(default=0)
	costo  = models.DecimalField(max_digits=100,decimal_places=2,default=0)
	distribuidor = models.DecimalField(max_digits=100,decimal_places=2,default=0)
	mayorista = models.DecimalField(max_digits=100,decimal_places=2,default=0)
	efectivo = models.DecimalField(max_digits=100,decimal_places=2,default=0)
	tarjeta = models.DecimalField(max_digits=100,decimal_places=2,default=0)

