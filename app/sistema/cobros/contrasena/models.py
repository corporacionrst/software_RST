# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


from ....sistema.usuarios.models import USUARIO_TIENDA
from ....sistema.tienda.models import EMPRESA
from ....cliente_proveedor.proveedor.models import PROVEEDOR

class CONTRASENA_ACTUAL(models.Model):
	proveedor = models.ForeignKey(PROVEEDOR,related_name="pass_proveedor")
	tienda = models.ForeignKey(EMPRESA,related_name="pass_store")
	actual= models.IntegerField(default=1)

class CONTRASENA(models.Model):
	no = models.AutoField(primary_key=True)
	ubicado = models.ForeignKey(CONTRASENA_ACTUAL)
	fehca_registro = models.DateField(auto_now=False,auto_now_add=False)
	correlativo = models.IntegerField(default=1)
	total = models.DecimalField(max_digits=300,decimal_places=4,default=0)
