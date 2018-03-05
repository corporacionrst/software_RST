# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from ...request_session import OKconta,OKpeople,getPerfil
from django.db.models import Q
from .models import PROVEEDOR
from ..persona.models import PERSONA
import json


# completa la busqueda de un proveedor por su NIT
# class completar_con_nombre(TemplateView):
# 	def get(self,request,*args,**kwargs):
# 		if OKpeople(request):
# 			nit = request.GET['nit']
# 			ppl = PERSONA.objects.get(nit=nit)
# 			pr = PROVEEDOR.objects.get(info=ppl)



class ver_proveedores(TemplateView):
	template_name="cliente_proveedor/proveedores/proveedor.html"
	def get(self,request,*args,**kwargs):
		context={}
		if OKconta(request):
			return render(request,self.template_name,context)
		else:
			return redirect("/")



class consultar_nit(TemplateView):
	def get(self,request,*args,**kwargs):
		try:
			if OKpeople(request):
				tienda=getPerfil(request).tienda
				nit = request.GET['nit'].upper()
				persona = PERSONA.objects.get(nit=nit)
				qs = PROVEEDOR.objects.filter(info=persona).filter(store=tienda)
				if qs.exists():
					qs=qs.values('info__nit','info__nombre','info__direccion','credito')
					qs=json.dumps(list(qs),cls=DjangoJSONEncoder)
					return HttpResponse(qs,content_type='application/json')
			return HttpResponse("{}",content_type='application/json')
		except:
			return HttpResponse("{}",content_type='application/json')	
		return HttpResponse("{}",content_type='application/json')


	
class consultar_nombre(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			tienda=getPerfil(request).tienda
			nombre = request.GET['nombre']
			i=int(request.GET['pag'])*3
			qs = PROVEEDOR.objects.filter(Q(info__nombre__icontains=nombre)).filter(store=tienda).values('info__nit','info__nombre')[i:i+2]
			qs=json.dumps(list(qs),cls=DjangoJSONEncoder)
			return HttpResponse(qs,content_type='application/json')
		return HttpResponse("{}",content_type='application/json')



class registrar_proveedor(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			nit=request.GET["nit"]
			comentario=request.GET["comentario"]
			credito=request.GET["credito"]
			monto=request.GET["monto"]
			dias=request.GET["dias"]
			persona = PERSONA.objects.filter(nit=nit)
			if persona.exists():
				pr = PROVEEDOR.objects.filter(nit=persona)
				if pr.exists():
					return HttpResponse("-1",content_type='text')
			else:
				nombre=request.GET["nombre"]
				direccion=request.GET["direccion"]
				telefono=request.GET["telefono"]
				correo=request.GET["correo"]
				persona=PERSONA()
				persona.nit = nit
				persona.nombre= nombre
				persona.direccion =direccion
				persona.telefono = telefono
				persona.correo =correo
				persona.save()
			pr = PROVEEDOR()
			pr.info=persona
			pr.comentario=comentario
			pr.credito=credito
			pr.monto=monto
			pr.dias_credito=dias
			pr.save()
			HttpResponse(nit+" fue creado satisfactoriamente",content_type='text')
		return HttpResponse("-1",content_type='text')
