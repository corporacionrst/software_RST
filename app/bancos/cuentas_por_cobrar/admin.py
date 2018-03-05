# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(LISTA_RECIBOS)
admin.site.register(DOCUMENTO_POR_COBRAR)
admin.site.register(DOCUMENTO_RECIBOS)


