# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from ..persona.models import PERSONA
from ...sistema.tienda.models import EMPRESA

class PROVEEDOR(models.Model):
	# 481377-4  : True  : 50,000 : 30
	info=models.ForeignKey(PERSONA)
	comentario=models.CharField(max_length=300,default="")
	credito = models.BooleanField(default=False)
	monto=models.DecimalField(max_digits=100,decimal_places=2,default=0)
	saldo=models.DecimalField(max_digits=100,decimal_places=2,default=0)
	dias_credito = models.IntegerField(default=0)
	store = models.ForeignKey(EMPRESA,null=True)