# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from ....productos.inventario.historial.models import HISTORIAL
from ...usuarios.models import Perfil
from ...tienda.models import EMPRESA

class CORRELATIVO_RECIBOS(models.Model):
	tienda = models.ForeignKey(EMPRESA)
	usuario = models.ForeignKey(Perfil)
	correlativo=models.IntegerField(default=1)


class LISTA_RECIBOS(models.Model):
	recibo=models.ForeignKey(CORRELATIVO_RECIBOS)
	correlativo=models.IntegerField(default=1)
	lista_documentos=models.ForeignKey(HISTORIAL)