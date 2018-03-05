# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ...sistema.usuarios.models import Perfil
from ...sistema.tienda.models import EMPRESA

# Create your models here.

class BANCO(models.Model):
	nombre = models.CharField(max_length=50, primary_key=True)
	def __unicode__(self):
		return self.nombre

class CUENTA_BANCARIA(models.Model):
	id=models.AutoField(primary_key=True)
	banco = models.ForeignKey(BANCO)
	tienda = models.ForeignKey(EMPRESA)
	administra= models.ForeignKey(Perfil,null=True)
	numero_de_cuenta = models.CharField(max_length=100)
	capital = models.DecimalField(max_digits=300,decimal_places=2,default=0)