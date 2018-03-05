# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from ....request_session import getPerfil,OKbodega
from django.views.generic import TemplateView
from ...usuarios.models import Perfil
from django.db.models import Q
from django.http import HttpResponse


import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from ....productos.inventario.historial.models import LISTA_PRODUCTO
from ....productos.inventario.inventario.models import INVENTARIO
from django.db import connection
class id_faltantes(TemplateView):
	template_name="sistema/bodega/lista_negativos.html"
	def get(self,request,id=None,*args,**kwargs):
		if OKbodega(request):
			inv = INVENTARIO.objects.get(id=id)
			usu=getPerfil(request)
			lp = LISTA_PRODUCTO.objects.filter(producto=inv.producto).filter(lista__ubicado__tienda=inv.tienda).filter(lista__tipo_doc="V").order_by("-created_date")[0:10]
			context={
				"pr":inv,
				"producto":lp,
				"tienda":usu.tienda
			}
			return render(request,self.template_name,context)
		return redirect("/")

class faltantes(TemplateView):
	template_name="sistema/bodega/negativo.html"
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			usu = getPerfil(request)
			inv = INVENTARIO.objects.filter(tienda=usu.tienda).filter(cantidad__lt=0)
			context={
				"inv":inv,
				"tienda":usu.tienda
			}
			return render(request,self.template_name,context)

		return redirect("/")

class lista(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			usu = getPerfil(request)
			Lista=LISTA_PRODUCTO.objects.filter(lista__ubicado__tienda=usu.tienda).filter(entregado__isnull=True)
			Lista=Lista.values("producto__codigo__nombre","producto__descripcion__detalle","producto__marca__nombre","cantidad","id","lista__ubicado__usuario__usuario__username")
			Lista=json.dumps(list(Lista),cls=DjangoJSONEncoder)
			return HttpResponse(Lista,content_type='application/json')
		return HttpResponse("{}",content_type="application/json")


class quitar(TemplateView):
	def post(self,request,*args,**kwargs):
		mensaje="{}"
		if OKbodega(request):
			lp=request.POST["id"]
			usuario=request.POST["usu"]
			usu = Perfil.objects.filter(usuario__id=usuario)[0]
			Lista=LISTA_PRODUCTO.objects.get(id=lp)
			Lista.entregado=usu
			Lista.save()
		return HttpResponse("V",content_type="application/json")
				


class cola(TemplateView):
	template_name="impresion/cola_socket.html"
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			usu = getPerfil(request)
			bod = Perfil.objects.filter(Q(puesto__nombre__icontains="BODEGA")).filter(tienda=usu.tienda)
			context={
				"tienda":usu.tienda,
				"id_t":usu.tienda.id,
				"bodega":bod,
			}
			return render(request,self.template_name,context)
		return redirect("/")


class bodega_index(TemplateView):
	template_name="sistema/bodega/index.html"
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			return render(request,self.template_name)
		return redirect("/")
