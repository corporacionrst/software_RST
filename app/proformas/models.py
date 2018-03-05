# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from ..sistema.usuarios.models import Perfil,DOCUMENTO_POR_TIENDA

# Create your models here.
class PROFORMA(models.Model):
	atencion= models.CharField(max_length=200,blank=True)
	telefono=models.CharField(max_length=20,blank=True)
	correo=models.CharField(max_length=100,blank=True)
	fehca_registro = models.DateField(auto_now=False,auto_now_add=False)
	fecha_vencimiento = models.DateField(auto_now=False,auto_now_add=False)
	vendedor=models.ForeignKey(Perfil)
	lista=models.OneToOneField(DOCUMENTO_POR_TIENDA)
	