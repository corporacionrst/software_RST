# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ....bancos.banco.models import CUENTA_BANCARIA

# Create your models here.

class DEPOSITOS(models.Model):
	fecha_registro = models.DateField(auto_now=False,auto_now_add=True,blank=True)
	cuenta_debitada= models.ForeignKey(CUENTA_BANCARIA,related_name="de")
	cuenta_acreditada=models.ForeignKey(CUENTA_BANCARIA,related_name="para")
	documento = models.CharField(max_length=300,default="")
	monto = models.DecimalField(max_digits=300,decimal_places=2,default=0)
	visto = models.BooleanField(default=False)
	confirmar=models.BooleanField(default=False)