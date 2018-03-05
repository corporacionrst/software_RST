# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *

admin.site.register(CODIGO)

admin.site.register(DESCRIPCION)

admin.site.register(SET)

admin.site.register(PRODUCTO_IMAGEN)
admin.site.register(IMAGENES)

@admin.register(PRODUCTO)
class VER_PRODUCTO(admin.ModelAdmin):
	list_display=("codigo","descripcion","marca","detalles","id_set")

@admin.register(PRODUCTO_SET)
class VER_PRODUCTO_SET(admin.ModelAdmin):
	list_display=[
	"id_set",
	"producto",
	"cantidad"
	]
