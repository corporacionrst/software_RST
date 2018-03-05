# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect

from django.views.generic import TemplateView
from ...request_session import OKcobros,getPerfil
from .models import DOCUMENTO_POR_COBRAR
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json

import datetime
from datetime import date, timedelta

class cola(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKcobros(request):
			pag=int(request.GET['pag'])*10
			orden=int(request.GET['orden'])
			if orden>0 and orden<4:
				usu = getPerfil(request)
				dia =date.today()+timedelta(days=1)
				dpc = DOCUMENTO_POR_COBRAR.objects.filter(documento__lista__ubicado__tienda=usu.tienda).exclude(fecha_limite__gt=dia)
				if orden==1:
					dpc.order_by("-fecha_limite")
				dpc=dpc.values("id","documento__lista__total","documento__lista__descuento","documento__cliente_proveedor__nit","documento__cliente_proveedor__nombre","pendiente")
				dpc=json.dumps(list(dpc),cls=DjangoJSONEncoder)
				return HttpResponse(dpc,content_type='application/json')
		return HttpResponse("{}",content_type="application/json")
		


			

class pendientes(TemplateView):
	template_name="sistema/cobros/recibos/pendientes.html"
	def get(self,request,*args,**kwargs):
		if OKcobros(request):
			usu = getPerfil(request)
			dpc = DOCUMENTO_POR_COBRAR.objects.filter(documento__lista__ubicado__tienda=usu.tienda).count()
			context={
				"pendientes":dpc,
				"tienda":usu.tienda.nombre,
			}
			return render(request,self.template_name,context)


		return redirect("/")

class menu(TemplateView):
	template_name="sistema/cobros/recibos/index.html"
	def get(self,request,*args,**kwargs):
		if OKcobros(request):
			usu = getPerfil(request)
			dpc = DOCUMENTO_POR_COBRAR.objects.filter(documento__lista__ubicado__tienda=usu.tienda).count()
			context={
				"pendientes":dpc
			}
			return render(request,self.template_name,context)
		return redirect("/")