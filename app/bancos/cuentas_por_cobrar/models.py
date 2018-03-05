# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


from ...productos.inventario.historial.models import HISTORIAL
from ...sistema.usuarios.models import Perfil
from ...sistema.tienda.models import EMPRESA

class LISTA_RECIBOS(models.Model):
	tienda = models.ForeignKey(EMPRESA)
	caja = models.ForeignKey(Perfil)
	correlativo=models.IntegerField(default=1)


class DOCUMENTO_POR_COBRAR(models.Model):
	documento = models.ForeignKey(HISTORIAL)
	fecha_limite= models.DateField(auto_now=False, auto_now_add=False)
	pendiente = models.DecimalField(max_digits=300,decimal_places=4,default=0)
	
class DOCUMENTO_RECIBOS(models.Model):
	Recibo_tienda=models.ForeignKey(LISTA_RECIBOS)
	fecha_limite= models.DateField(auto_now=False, auto_now_add=False)
	correlativo=models.IntegerField()
