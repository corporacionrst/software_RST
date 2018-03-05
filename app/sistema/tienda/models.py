# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class EMPRESA(models.Model):
	# 1 : CENTRAL : Petapa z 12  : 2208-1414
	# 2 : COBAN   : Alta verapaz : 2334-1231
	# 3 : TERMINAL: Zona 9		 : 2331-5353
	id=models.AutoField(primary_key=True)
	nombre=models.CharField(max_length=20)
	direccion=models.CharField(max_length=200)
	telefono=models.CharField(max_length=15)
	nit=models.CharField(max_length=15,default="")
	def __unicode__(self):
		return unicode(self.nombre)