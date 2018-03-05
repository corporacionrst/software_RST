# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(HISTORIAL)
class HIS(admin.ModelAdmin):
	list_display=('documento','cliente_proveedor','fehca_registro','fecha_documento','ingresa','lista')

@admin.register(LISTA_PRODUCTO)
class LP(admin.ModelAdmin):
	list_display=('producto','cantidad','unitario','entregado')





admin.site.register(RECIBO)
admin.site.register(CORRELATIVO_INFILE)
admin.site.register(INFILE)

admin.site.register(RECHAZO_IMPRESION)

admin.site.register(RECORD_DE_VENTAS)