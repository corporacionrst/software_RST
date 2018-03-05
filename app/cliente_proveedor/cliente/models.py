# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from ..persona.models import PERSONA
from ...sistema.tienda.models import EMPRESA
from ...sistema.usuarios.models import Perfil

class CLIENTE(models.Model):
	info=models.ForeignKey(PERSONA)
	comentario=models.CharField(max_length=300,default="")
	credito = models.BooleanField(default=False)
	monto=models.DecimalField(max_digits=100,decimal_places=2,default=0)
	saldo=models.DecimalField(max_digits=100,decimal_places=2,default=0)
	dias_credito = models.IntegerField(default=0)
	store = models.ForeignKey(EMPRESA,null=True)
	vendedor = models.ForeignKey(Perfil,null=True)
	mayorista=models.BooleanField(default=False)