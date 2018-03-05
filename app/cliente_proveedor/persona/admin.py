# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import PERSONA



@admin.register(PERSONA)
class VER_PERSONA(admin.ModelAdmin):
	list_display=("nit","nombre","direccion","telefono","correo")