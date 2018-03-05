# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse

from django.views.generic import TemplateView
from django.core.serializers.json import DjangoJSONEncoder

import json

from .models import LISTA_PRODUCTO
from ....request_session import OKpeople
from .tasks import rechazar_impresion

class listar_producto(TemplateView):
	def get(self,request,*args,**kwargs):
		i = int(request.GET['pag'])*10
		documento = request.GET["documento"]
		lp = LISTA_PRODUCTO.objects.filter(lista=documento)
		pdm="producto__marca__definicion"
		if lp.exists():
			lp=lp.values('producto__codigo','producto__descripcion',pdm,'cantidad','unitario')[i:i+10]
			lp=json.dumps(list(lp),cls=DjangoJSONEncoder)
			return HttpResponse(lp,content_type='application/json')	
		return HttpResponse("{}",content_type='application/json')

def rechazo_de_impresion(documento,motivo,reply_channel):
	task=rechazar_impresion.delay(documento,motivo,reply_channel)