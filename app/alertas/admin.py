# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import ALERTA




@admin.register(ALERTA)
class VER_ALERTA(admin.ModelAdmin):
	list_display=("tipo","mensaje","sub_mensaje","requiere","ruta","visto","puesto","tienda")

