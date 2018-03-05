
from __future__ import unicode_literals
from django.db import models


class TIPO_DE_MEDIDA(models.Model):
	# unidades    : u
	# pies        : ft
	# metros      : m
	# centimetros : cm
	# libras      : lb
	nombre = models.CharField(max_length=20,primary_key=True)
	acortado = models.CharField(max_length=4)
	def __unicode__(self):
		return unicode(self.nombre)

class DETALLE(models.Model):
	# DIAMETRO INTERNO
	# DIAMETRO EXTERNO
	# ALTURA
	# LONGITUD
	id= models.CharField(max_length=50,primary_key=True)
	def __unicode__(self):
		return unicode(self.id)

class LISTA_DETALLES(models.Model):
	#1: DIAMETRO INTERNO : 25 : milimetros
	#2: DIAMETRO EXTERNO : 2  : pulgadas
	#3: ALTURA           : 17 : milimetros
	#4: LONGITUD         : 1  : pies	
	id = models.AutoField(primary_key=True)
	detalle=models.ForeignKey(DETALLE)
	dimension=models.DecimalField(max_digits=10,decimal_places=2,default=0)
	tipo=models.ForeignKey(TIPO_DE_MEDIDA)
	def __unicode__(self):
		cad =str(self.detalle)+":::"+str(self.dimension)+":"+str(self.tipo)
		return unicode(cad)

class LISTADO_DET(models.Model):
	id = models.AutoField(primary_key=True)
	def __unicode__(self):
		return unicode(self.id)

class FICHA_TECNICA(models.Model):
	listado = models.ForeignKey(LISTADO_DET)
	detalle = models.ForeignKey(LISTA_DETALLES)

	
