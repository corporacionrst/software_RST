# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from ....sistema.tienda.models import EMPRESA
from ....sistema.usuarios.models import Perfil
from ....productos.producto.models import PRODUCTO


class NO_TRASLADO(models.Model):
	de = models.ForeignKey(EMPRESA,related_name="envia_traslado")
	a=models.ForeignKey(EMPRESA,related_name="recibe_traslado")
	numero=models.IntegerField(default=1)
	total=models.DecimalField(decimal_places=4,max_digits=500,default=0)
	

class TRASLADO(models.Model):
	no=models.ForeignKey(NO_TRASLADO)
	fecha=models.DateField(auto_now=False,auto_now_add=False,null=True)
	numero=models.IntegerField(default=1)
	producto = models.ForeignKey(PRODUCTO)
	cantidad = models.IntegerField(default=0)
	venta=models.DecimalField(decimal_places=4,max_digits=300,default=0)

	
class TRASLADO_AUTORIZADO(models.Model):
	no =models.ForeignKey(NO_TRASLADO)
	indice=models.IntegerField(default=0)
	solicita=models.ForeignKey(Perfil,null=True,related_name="traslado_solicita")
	autoriza=models.ForeignKey(Perfil,null=True,related_name="traslado_autoriza")
	autorizada=models.BooleanField(default=False)
	recibe = models.CharField(max_length=200,default="")

class MERCADERIA_A_CANCELAR(models.Model):
	producto=models.ForeignKey(TRASLADO)
	cantidad=models.IntegerField()

class DOCUMENTO_A_CANCELAR(models.Model):
	emite_cobro = models.ForeignKey(EMPRESA,related_name="emite_pago")
	recibe_cobro=models.ForeignKey(EMPRESA,related_name="recibe_pago")
	monto=models.DecimalField(decimal_places=4,max_digits=300,default=0)
	lista_a_cancelar = models.ManyToManyField(MERCADERIA_A_CANCELAR)



