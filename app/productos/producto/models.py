# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from ..marca.models import *
from ..detalle.models import *


class CODIGO(models.Model):
	# UC205-16, 
	# P205  ,
	# UCP205-16
	# FT40-1
	# 40-1
	# CL40-1
	nombre = models.CharField(max_length=300,primary_key=True)
	def __unicode__(self):
		return unicode(self.nombre)

class DESCRIPCION(models.Model):
	# COJINETE 
	# HOUSING
	# CHUMACERA
	# UNION
	# CADENA 
	detalle = models.CharField(max_length=1000,primary_key=True)
	def __unicode__(self):
		return unicode(self.detalle)


class SET(models.Model):
	# 1
	# 2
	# 3
	numero=models.CharField(max_length=300,primary_key=True,default="-")
	def __unicode__(self):
		return unicode(self.numero)


class PRODUCTO(models.Model):
	# 1 : UC205-16  : COJINETE           : TRANSLINK
	# 2 : P205      : HOUSING            : TRANSLINK
	# 3 : UCP205-16 : CHUMACERA DE BANCO : TRANSLINK
	# 4 : FT40-1	: PIE DE CADENA 	 : TRANSLINK
	# 6 : CL40-1	: UNION PARA CADENA  : TRANSLINK
	# 5 : 40-1		: CAJA DE CADENA	 : TRANSLINK
	id = models.AutoField(primary_key=True)
	codigo = models.ForeignKey(CODIGO)
	descripcion = models.ForeignKey(DESCRIPCION)
	marca = models.ForeignKey(MARCA)
	detalles = models.ForeignKey(LISTADO_DET,null=True)
	id_set = models.ForeignKey(SET,null=True,blank=True)
	def __unicode__(self):
			return unicode(self.codigo)


class IMAGENES(models.Model):
	imagen = models.CharField(max_length=5000,default="")
	def __unicode__(self):
		return unicode(self.imagen)
	
	

class PRODUCTO_IMAGEN(models.Model):
	producto = models.ForeignKey(PRODUCTO)
	imagen = models.ForeignKey(IMAGENES)

class PRODUCTO_SET(models.Model):
	id_set = models.ForeignKey(SET, related_name='id_set')
	producto = models.ForeignKey(PRODUCTO,related_name='producto')
	cantidad = models.IntegerField()
	def __unicode__(self):
		return unicode(self.producto)





