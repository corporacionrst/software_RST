# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.utils import timezone
from ....cliente_proveedor.persona.models import PERSONA
from ....sistema.usuarios.models import Perfil,DOCUMENTO_POR_TIENDA
from ....sistema.tienda.models import EMPRESA
from ...producto.models import PRODUCTO

from ....sistema.cobros.cobro.models import DOCUMENTOS_POR_CAJA

class HISTORIAL(models.Model):
	id = models.AutoField(primary_key=True)
	serie = models.CharField(max_length=5,default="")
	documento = models.CharField(max_length=300)
	cliente_proveedor= models.ForeignKey(PERSONA)
	fehca_registro = models.DateField(auto_now=False,auto_now_add=False)
	fecha_documento = models.DateField(auto_now=False,auto_now_add=True)
	ingresa=models.ForeignKey(Perfil)
	lista=models.OneToOneField(DOCUMENTO_POR_TIENDA)
	
class LISTA_PRODUCTO(models.Model):
	lista=models.ForeignKey(DOCUMENTO_POR_TIENDA)
	created_date = models.DateTimeField('date created', default=timezone.now)
	producto = models.ForeignKey(PRODUCTO)
	cantidad = models.IntegerField(default=0)
	unitario = models.DecimalField(max_digits=300,decimal_places=4,default=0)
	entregado=models.ForeignKey(Perfil,null=True,blank=True,default=None)

class RECIBO(models.Model):
	tienda=models.ForeignKey(EMPRESA)
	caja = models.ForeignKey(Perfil)
	correlativo=models.IntegerField(default=1)


class CORRELATIVO_INFILE(models.Model):
	serie = models.ForeignKey(DOCUMENTOS_POR_CAJA)
	documento = models.OneToOneField(HISTORIAL)
	fecha_creacion=models.DateField(auto_now=False,auto_now_add=False)
	fecha_a_registrar=models.DateField(auto_now=False,auto_now_add=False)


class INFILE(models.Model):
	documento = models.ForeignKey(CORRELATIVO_INFILE)
	correlativo=models.IntegerField()
	huella=models.CharField(max_length=300,default="")


class RECHAZO_IMPRESION(models.Model):
	fecha_eliminacion = models.DateField(auto_now=False,auto_now_add=False)
	documento = models.ForeignKey(HISTORIAL)
	motivo = models.CharField(max_length=200)


class RECORD_DE_VENTAS(models.Model):
	user = models.ForeignKey(Perfil,related_name="vendedor")
	tienda=models.ForeignKey(EMPRESA,related_name="tienda_facturada")
	month=models.IntegerField()
	year=models.IntegerField()
	record=models.DecimalField(max_digits=300,decimal_places=4,default=0)
	facturas = models.ManyToManyField(HISTORIAL,related_name="documentos",blank=True)

