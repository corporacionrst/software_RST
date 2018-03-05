# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *
# Register your models here.


class View_Lista(admin.ModelAdmin):
	list_display=[
	"detalle",
	"dimension",
	"tipo",
	]

admin.site.register(LISTA_DETALLES,View_Lista)


admin.site.register(TIPO_DE_MEDIDA)
admin.site.register(DETALLE)
admin.site.register(LISTADO_DET)
admin.site.register(FICHA_TECNICA)


