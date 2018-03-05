# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import PROVEEDOR

@admin.register(PROVEEDOR)
class VER_PRODUCTO(admin.ModelAdmin):
	list_display=("info","comentario","credito","monto","dias_credito","store")