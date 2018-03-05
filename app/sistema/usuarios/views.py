# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from .models import Perfil,PERMISOS
from ...request_session import *
from .forms import crear_usuario
from ...productos.inventario.historial.models import RECORD_DE_VENTAS

from django.contrib.auth.models import User

from django.contrib import messages

from datetime import date,datetime

class seguimiento(TemplateView):
	meta=100000
	def get(self,request,*args,**kwargs):
		labels=[]
		default_val=[]
		bgcolor=[]	
		user = int(request.GET['usuario'])
		if OKadmin(request):
			user=Perfil.objects.get(id=user)
			usu = getPerfil(request)
			year=date.today().year-1
			record =RECORD_DE_VENTAS.objects.filter(user=user).filter(tienda=user.tienda).filter(year__gte=year)
			for r in record:
				labels.append(str(r.month)+"/"+str(r.year))
				record=r.record
				default_val.append(record)
				if record<(self.meta/4):
					bgcolor.append('rgba(255, 99, 132, 0.2)')
				elif record<(self.meta/2):
					bgcolor.append('rgba(153, 102, 255, 0.2)')
				elif record<self.meta:
					bgcolor.append('rgba(255, 159, 64, 0.2)')
				else:
					bgcolor.append('rgba(54, 162, 235, 0.2)',)

		data={
			"labels":labels,
			"default_val":default_val,
			"bgcolor":bgcolor
		}
		return JsonResponse(data)
		
		



class historial(TemplateView):
	template_name='sistema/admin/usuarios/historial.html'
	tienda =crear_usuario
	def get(self,request,id=None,*args,**kwargs):
		pr = Perfil.objects.get(id=id)
		fecha = datetime.strptime('Jan 1 '+str(datetime.now().year)+'  1:33PM', '%b %d %Y %I:%M%p')
		permisos=PERMISOS.objects.filter(Perfil=pr).filter(fecha__gte=fecha).count()
		if OKadmin(request):
			context ={
				"usuario":pr,
				"fecha_inicia":pr.fecha_ingreso,
				"ultima_indemnizacion":pr.ultima_indemnizacion,
				"total_permisos":permisos,
			}
			return render(request,self.template_name,context)
		else:
			return render(request,"administracion/E404.html",{})
	def post(self,request,id=None,*args,**kwargs):
		val = getPerfil(request)
		if OKadmin(request):
			form = self.tienda(request.POST or None, request.FILES or None)
			if form.is_valid():
				perfil = Perfil.objects.filter(usuario=id)[0]
				perfil.nombre = form.cleaned_data['nombre']
				perfil.apellido= form.cleaned_data['apellido']
				perfil.direccion =form.cleaned_data['direccion']
				perfil.puesto = form.cleaned_data['puesto'] 
				perfil.tienda = val.tienda
				perfil.fecha_nacimiento= form.cleaned_data['fecha_de_nacimiento']
				perfil.fecha_ingreso = form.cleaned_data['fecha_ingreso']
				perfil.multitienda=False
				perfil.cui=form.cleaned_data['cui_o_dpi']
				perfil.no_igss=form.cleaned_data['numero_de_igss']
				perfil.save()
				messages.success(request,usu+" creado satisfactoriamente")
			else:
				messages.error(request,"error al crearX2")
			context ={
				"form":form,
			}
			return render(request,self.template_name,context)
		else:
			return redirect("/")





# Create your views here.
class usuarios(TemplateView):
	template_name='sistema/admin/usuarios/usuarios.html'
	def get(self,request,*args,**kwargs):
		if OKadmin(request):
			val = Perfil.objects.get(usuario=request.user)
			queryset = Perfil.objects.all().filter(tienda=val.tienda.id)
			context ={
				"objeto":queryset,
				"empresa":val.tienda,
				"usuario":val.usuario,
			}
			return render(request,self.template_name,context)
		else:
			return render(request,"administracion/E404.html",{})

class agregar_usuario(TemplateView):
	template_name='sistema/admin/usuarios/agregar.html'
	tienda =crear_usuario
	initial = {'key': 'value'}
	def get(self,request,*args,**kwargs):
		form = self.tienda(initial=self.initial)
		if OKadmin(request):
			context ={
				"form":form,
			}
			return render(request,self.template_name,context)
		else:
			return render(request,"administracion/E404.html",{})
	def post(self,request,*args,**kwargs):
		val = getPerfil(request)
		if OKadmin(request):
			form = self.tienda(request.POST or None, request.FILES or None)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.save()	
				usu=instance.username
				perfil = Perfil()
				perfil.usuario = instance
				perfil.nombre = form.cleaned_data['nombre']
				perfil.apellido= form.cleaned_data['apellido']
				perfil.direccion =form.cleaned_data['direccion']
				perfil.telefono = form.cleaned_data['telefono']
				perfil.puesto = form.cleaned_data['puesto'] 
				perfil.tienda = val.tienda
				perfil.fecha_nacimiento= form.cleaned_data['fecha_de_nacimiento']
				perfil.fecha_ingreso = form.cleaned_data['fecha_ingreso']
				perfil.documento4 = "4~"+usu+"~1"
				perfil.multitienda=False
				indem =form.cleaned_data['ultima_indmemnizacion']
				if indem==None or indem=="":
					indem=date.today()
				perfil.ultima_indemnizacion=indem
				perfil.cui=form.cleaned_data['cui_o_dpi']
				perfil.no_igss=form.cleaned_data['numero_de_igss']

				perfil.save()
				messages.success(request,usu+" creado satisfactoriamente")
				
			else:
				messages.error(request,"error al crear")
			context ={
				"form":form,
			}
			return render(request,self.template_name,context)
		else:
			return redirect("/")


class eliminar_usuario(TemplateView):
	def get(self,request,*args,**kwargs):
		usu = int(request.GET['usuario'])
		usu = User.objects.get(id=usu)
		usu.delete()
		return HttpResponse('{"usu":"eliminado correctamente"}',content_type='application/json')



