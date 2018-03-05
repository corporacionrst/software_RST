# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#DJANGO
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.http import HttpResponse

from django.views.generic import TemplateView
from django.db.models import Q
# PROPIAS
from ..sistema.usuarios.models import Perfil,PERMISOS
from ..request_session import *
from .forms import *
from datetime import date,datetime
from django.http import JsonResponse

from ..productos.inventario.historial.models import RECORD_DE_VENTAS

from django.core.serializers.json import DjangoJSONEncoder
import json

from .forms import formulario_permisos

class permisos(TemplateView):
	template_name="sistema/permisos/"
	formulario=formulario_permisos
	initial = {'key': 'value'}
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			usu=getPerfil(request)
			form = self.formulario(initial=self.initial)
			context={
				"tienda":usu.tienda,
				"form":form
			}
			pl = self.template_name+obtenerPlantilla(request)
			return render(request,pl,context)
		return redirect("/")
	def post(self,request,*args,**kwargs):
		form = self.formulario(request.POST)
		if form.is_valid():
			de = (form.cleaned_data['de']).split("-")
			de=date(int(de[0]),int(de[1]),int(de[2]))
			a = (form.cleaned_data['a']).split("-")
			a=date(int(a[0]),int(a[1]),int(a[2]))
			usu = getPerfil(request)
			year=date.today().year
			fecha = date(year,1,1)
			permisos=PERMISOS.objects.filter(Perfil=usu).filter(fecha__gte=fecha).filter(motivo="").filter(autorizado=False).count()

			delta=(a-de).days

			if delta>0 and delta-permisos<15:
				print permisos
				print "si, vale"
			else:
				print "no vale"
		return redirect("/permisos")





class get_data(TemplateView):
	meta=100000
	def get(self,request,*args,**kwargs):
		labels=[]
		default_val=[]
		bgcolor=[]	
		if OKadmin(request):
			usu=getPerfil(request)
			mes=date.today().month
			year=date.today().year
			record =RECORD_DE_VENTAS.objects.filter(tienda=usu.tienda).filter(month=mes).filter(year=year)
			for r in record:
				labels.append(r.user.usuario.username)
				record=r.record
				default_val.append(record)
				if record<(self.meta/4):
					bgcolor.append('rgba(255, 99, 132, 0.2)')
				elif record<(self.meta/2):
					bgcolor.append('rgba(153, 102, 255, 0.2)')
				elif record<self.meta:
					bgcolor.append('rgba(255, 159, 64, 0.2)')
				else:
					bgcolor.append(
                'rgba(54, 162, 235, 0.2)',)

		data={
			"labels":labels,
			"default_val":default_val,
			"bgcolor":bgcolor
		}
		return JsonResponse(data)
		
		


class index(TemplateView):
	main = "website/sitio/index.html"
	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated():
			if OKadmin(request):
				context={
					"hoy":date.today()
				}
				return render(request,"sistema/admin/index.html",context)
			elif OKbodega(request):
				return render(request,"sistema/bodega/index.html")
			elif OKconta(request):
				return render(request,"sistema/conta/index.html")
			elif OKcobros(request):
				return render(request,"sistema/cobros/index.html")
			elif OKventas(request):
				return render(request,"sistema/ventas/index.html")
			else :
				return render(request,"website/ERROR/E404.html",{})
		else:
			consulta = request.GET.get("q")
			if consulta:
				consulta_lista = consulta_lista.filter()
		queryset = ""
		context ={
			"objeto":queryset,
			"titulo":"Noticias",
		}
		return redirect("/sesion")

class sesion(TemplateView):
	plantilla="website/sitio/login.html"
	initial = {'key': 'value'}
	login_form = LoginForm
	def get(self,request,*args,**kwargs):
		form = self.login_form(initial=self.initial)
		return render(request,self.plantilla,{'form':form})
	def post(self,request,*args,**kwargs):
		form = self.login_form(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('/')
			messages.error(request," usuario o password incorrectos")
			return render(request,self.plantilla,{'form':form})
		else:
			return render(request,self.plantilla,context)

class puesto(TemplateView):
	def get(self,request,*args,**kwargs):
		try:
			id_p = getPerfil(request)
			pr =Perfil.objects.filter(id=id_p).filter(Q(puesto__nombre__icontains=i))
			if pr.exists():
				return HttpResponse("V",content_type="text")
			return HttpResponse("F",content_type="text")
		except:
			return HttpResponse("F",content_type="text")


def fin_S(request):
	logout(request)
	return redirect('/')


def ap(request):
	return redirect("https://www.stackoverflow.com/admin.php")
