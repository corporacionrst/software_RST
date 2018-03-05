# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class PERSONA(models.Model):
	nit = models.CharField(max_length=30,primary_key=True)
	nombre= models.CharField(max_length=100)
	direccion = models.CharField(max_length=300)
	telefono = models.CharField(max_length=15)
	correo= models.CharField(max_length=50)
	password=models.CharField(max_length=200,null=True, default="")
	def __unicode__(self):
		return unicode(self.nombre)