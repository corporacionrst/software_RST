# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import  INVENTARIO

@admin.register(INVENTARIO)
class INV(admin.ModelAdmin):
	list_display=('tienda','producto','cantidad','costo','tarjeta')
