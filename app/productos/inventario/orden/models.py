# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ....cliente_proveedor.proveedor.models import PROVEEDOR
from ....sistema.usuarios.models import Perfil,DOCUMENTO_POR_TIENDA
from ..historial.models import HISTORIAL
from ....sistema.cobros.contrasena.models import CONTRASENA


class ORDEN_DE_COMPRA(models.Model):
	id = models.AutoField(primary_key=True)
	impreso = models.BooleanField(default=False)
	proveedor= models.ForeignKey(PROVEEDOR,default=1)
	fecha_registro = models.DateField(auto_now=False,auto_now_add=True,blank=True)
	solicita=models.ForeignKey(Perfil,related_name="solicitante")
	autorizo = models.ForeignKey(Perfil,related_name="autorizo",null=True)
	autorizada=models.BooleanField(default=False)
	comentario=models.CharField(max_length=300,default="")
	lista=models.ForeignKey(DOCUMENTO_POR_TIENDA)
	documento = models.ForeignKey(HISTORIAL,related_name="relacion_orden",default=1)
	doc_contra=models.ForeignKey(CONTRASENA,related_name="contrasena_id",null=True,default=None,blank=True)