# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import TRASLADO,NO_TRASLADO,TRASLADO_AUTORIZADO

admin.site.register(TRASLADO)
admin.site.register(NO_TRASLADO)
admin.site.register(TRASLADO_AUTORIZADO)