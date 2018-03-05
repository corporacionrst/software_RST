# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ...usuarios.models import Perfil
from ...tienda.models import EMPRESA


# Create your models here.
class DOCUMENTOS_POR_CAJA(models.Model):
	tienda = models.ForeignKey(EMPRESA)
	usuario = models.ForeignKey(Perfil)
	serie = models.CharField(max_length=5)
	control_interno =models.IntegerField(default=1)
	correlativo =models.IntegerField(default=1)