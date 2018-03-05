# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import CONTRASENA,CONTRASENA_ACTUAL
admin.site.register(CONTRASENA_ACTUAL)
# admin.site.register(CONTRASENA)



@admin.register(CONTRASENA)
class VER_CN(admin.ModelAdmin):
	list_display=("correlativo","ubicado","total")

