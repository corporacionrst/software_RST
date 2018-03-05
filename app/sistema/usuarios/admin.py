# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(PUESTO)
admin.site.register(Perfil)

@admin.register(USUARIO_TIENDA)
class VER_UT(admin.ModelAdmin):
	list_display=("usuario","tienda","orden","fac_1","fac_2","fac_3","fac_4")


@admin.register(DOCUMENTO_POR_TIENDA)
class VER_DXT(admin.ModelAdmin):
	list_display=("ubicado","pagina","correlativo","tipo_doc","credito","total")

admin.site.register(PERMISOS)


admin.site.register(SALARIO_MENSUAL)
