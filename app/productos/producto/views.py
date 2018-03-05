# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import TemplateView
from .forms import *
from .models import *


from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.contrib import messages

from ...request_session import OKbodega,sumar_DATO,OKpeople

from ...sistema.usuarios.models import Perfil

import json

# Create your views here.


class crear_producto(TemplateView):
	template_name = 'productos/producto/crear.html'
	producto_form    = FormProducto
	initial = {'key': 'value'}

	def get(self, request, *args, **kwargs):
		if OKbodega(request):
			id_set=Perfil.objects.get(usuario=request.user).documento4
			form = self.producto_form(initial=self.initial)
			context ={
				"form":form,
				"set":id_set 
			}
			return render(request, self.template_name, context)
		return redirect("/")

	def post(self,request,*args,**kwargs):
		if OKbodega(request):
			id_set=Perfil.objects.get(usuario=request.user).documento4
			form = self.producto_form(request.POST)
			context ={
				"form":form,
				"set":id_set 
			}
			return render(request, self.template_name, context)
		return redirect("/")

class consulta_pagina(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			producto=request.GET['codigo']
			i=int(request.GET['pagina'])*10
			if producto!="":
				qs = PRODUCTO.objects.filter(Q(codigo__nombre__icontains=producto)|Q(descripcion__detalle__icontains=producto)).values('id','codigo','descripcion','marca').order_by('codigo')[i:i+10]
				qs=json.dumps(list(qs),cls=DjangoJSONEncoder)
				return HttpResponse(qs,content_type='application/json')
		return HttpResponse("{}",content_type='application/json')


class consulta_pagina_set(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			producto=request.GET['codigo']
			i=int(request.GET['pagina'])*10
			if producto!="":
				qs = PRODUCTO_SET.objects.filter(id_set=producto).values('producto__codigo','producto__descripcion','producto__marca','cantidad')[i:i+10]
				qs=json.dumps(list(qs),cls=DjangoJSONEncoder)
				return HttpResponse(qs,content_type='application/json')
		return HttpResponse("{}",content_type='application/json')

class cargar_set(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			id_set = request.GET['set']
			producto = request.GET['producto']
			cantidad =request.GET['cantidad']
			set_no= SET.objects.filter(numero=id_set)
			if not set_no.exists():
				set_no=SET()
				set_no.numero=id_set
				set_no.save()	
			set_no=SET.objects.get(numero=id_set)
			producto=PRODUCTO.objects.get(id=producto)
			tstPs=PRODUCTO_SET.objects.filter(id_set=set_no).filter(producto=producto)
			if not tstPs.exists():
				store_set=PRODUCTO_SET()
				store_set.id_set=set_no
				store_set.producto = producto
				store_set.cantidad = int(cantidad)
				store_set.save()
			qs = PRODUCTO_SET.objects.filter(id_set=set_no).values('producto__codigo','producto__descripcion','producto__marca','cantidad')[:10]
			qs=json.dumps(list(qs),cls=DjangoJSONEncoder)							
			
			return HttpResponse(qs,content_type='application/json')
		return HttpResponse("{}",content_type='application/json')

class tabla_set(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			set_no= SET.objects.filter(numero=request.GET['set'])
			pag = int(request.GET['pag'])*10
			qs = PRODUCTO_SET.objects.filter(id_set=set_no).values('producto','producto__codigo','producto__descripcion','producto__marca','cantidad','id_set')[pag:pag+10]
			qs=json.dumps(list(qs),cls=DjangoJSONEncoder)
			return HttpResponse(qs,content_type='application/json')	
		return HttpResponse("{}",content_type='application/json')						
				

class quitar_set(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			producto= request.GET['producto']
			id_set = request.GET['set']
			PRODUCTO_SET.objects.filter(id_set=id_set).filter(producto=producto).delete()
			return HttpResponse("{}",content_type='application/json')	
	

class sumar_d3(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			return HttpResponse(sumar_DATO(request,"4"),content_type="text")


class set_producto(TemplateView):
	template_name = 'productos/producto/set.html'
	producto_form    = FormProducto
	initial = {'key': 'value'}

	def get(self, request, *args, **kwargs):
		if OKbodega(request):
			id_set=Perfil.objects.get(usuario=request.user).documento4
			form = self.producto_form(initial=self.initial)
			context ={
				"form":form,
				"set":id_set 
			}
			return render(request, self.template_name, context)
		return redirect("/")

	def post(self,request,*args,**kwargs):
		if OKbodega(request):
			id_set=Perfil.objects.get(usuario=request.user).documento4
			form = self.producto_form(request.POST)
			context ={
				"form":form,
				"set":id_set 
			}
			return render(request, self.template_name, context)
		return redirect("/")

class obtener_producto(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			pr = int(request.GET['producto'])
			qs = PRODUCTO.objects.get(id=pr).id_set
			if qs==None:
				qs=Perfil.objects.get(usuario=request.user).documento4
			return HttpResponse(qs,content_type='text')	
		return HttpResponse("{}",content_type='text')	
	
class asignar_set(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			pr = request.GET['producto']
			id_set = request.GET['set']
			p = PRODUCTO.objects.get(id=pr)
			p.id_set=SET.objects.get(numero=id_set)
			if str(Perfil.objects.get(usuario=request.user).documento4)==id_set:
				sumar_DATO(request,"4")
			p.save()
			return HttpResponse("si",content_type='text')	





