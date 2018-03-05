# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..sistema.usuarios.models import Perfil,PUESTO
from ..sistema.tienda.models import EMPRESA

# Create your models here.

class ALERTA(models.Model):
	# 0: alerta, 1: notificacion 2: listado_a_despachar
	tipo = models.IntegerField(default=0)
	mensaje = models.CharField(max_length=300,default="")
	sub_mensaje=models.CharField(max_length=300,default="")
	requiere=models.ForeignKey(Perfil)
	ruta = models.CharField(max_length=2000,default="")
	visto = models.BooleanField(default=False)
	puesto = models.ForeignKey(PUESTO)
	tienda =models.ForeignKey(EMPRESA,related_name="tienda_solicitud",default=1)
