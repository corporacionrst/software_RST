# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# from ..banco.models import CUENTA_BANCARIA
# from ...sistema.usuarios.models import Perfil
# # Create your models here.



# class CHEQUERA(models.Model):
# 	numero = models.CharField(max_length=200)
# 	banco = models.ForeignKey(CUENTA_BANCARIA)
# 	proximo_cheque= models.IntegerField()


# class CHEQUE(models.Model):
# 	chequera = models.ForeignKey(CHEQUERA)
# 	numero = models.IntegerField()
# 	monto = models.DecimalField(max_digits=300,decimal_places=2,default=0)
# 	solicita = models.ForeignKey(Perfil)