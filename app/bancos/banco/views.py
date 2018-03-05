# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.db.models import Q
# Create your views here.
from .forms import BancoForm,AsignaBanco

from .models import BANCO,CUENTA_BANCARIA

from ...request_session import OKadmin,OKcobros,getPerfil
from django.contrib import messages

from ...sistema.usuarios.models import Perfil

class depositar(TemplateView):
	template_name="bancos/depositar.html"
	def get(self,request,*args,**kwargs):
		if OKcobros(request):
			us = getPerfil(request)
			cuenta = CUENTA_BANCARIA.objects.filter(tienda=us.tienda).filter(administra__isnull=True)
			cuenta = CUENTA_BANCARIA.objects.filter(Q(puesto__nombre__icontains="ADMIN")|Q(puesto__nombre__icontains="COBROS"))


		return redirect("/")



class asignar_cuenta_bancos(TemplateView):
	template_name="bancos/asignar.html"
	def get(self,request,*args,**kwargs):
		if OKadmin(request):
			us = getPerfil(request)
			cuenta = CUENTA_BANCARIA.objects.filter(tienda=us.tienda).filter(administra__isnull=True)
			usuario = Perfil.objects.filter(tienda=us.tienda).filter(Q(puesto__nombre__icontains="ADMIN")|Q(puesto__nombre__icontains="COBROS"))
			context={
				"tienda":us.tienda,
				"cuenta":cuenta,
				"usuarios":usuario
			}
			return render(request,self.template_name,context)
		return redirect("/")
	def post(self,request,*args,**kwargs):
		if OKadmin(request):
			b= int(request.POST.get("banco"))
			usuario=int(request.POST.get("usuario"))
			us = Perfil.objects.filter(usuario__id=usuario)
			us=us[0]
			cuenta = CUENTA_BANCARIA.objects.filter(id=b)[0]
			cuenta.administra=us
			cuenta.save()
			cuenta = CUENTA_BANCARIA.objects.filter(tienda=us.tienda).filter(administra__isnull=True)
			usuario = Perfil.objects.filter(tienda=us.tienda).filter(Q(puesto__nombre__icontains="ADMIN")|Q(puesto__nombre__icontains="COBROS"))
			context={
				"tienda":us.tienda,
				"cuenta":cuenta,
				"usuarios":usuario
			}
			messages.success(request,"la cuenta ha sido asignada con exito")
			return render(request,self.template_name,context)
		return redirect("/")




class cuenta_bancos(TemplateView):
	template_name="bancos/cuentas.html"
	forms = AsignaBanco
	initial = {'key': 'value'}
	def get(self,request,*args,**kwargs):
		if OKadmin(request):
			tienda = getPerfil(request).tienda
			context={
			"form":self.forms(initial=self.initial),
			"tienda":tienda

			}
			return render(request,self.template_name,context)
		return redirect("/")
	def post(self,request,*args,**kwargs):
		if OKadmin(request):
			form = self.forms(request.POST)
			us = getPerfil(request).tienda
			if form.is_valid():
				banco = form.cleaned_data['banco']
				numero = form.cleaned_data['numero']
				monto = form.cleaned_data['monto']
				cb=CUENTA_BANCARIA.objects.filter(tienda=us).filter(banco=banco).filter(numero_de_cuenta=numero)
				if cb.exists():
					if cb[0].administra!=None:
						messages.error(request," esta cuenta ya esta registrada, es administrada por '"+cb[0].administra.usuario.username+"'")
					else:
						messages.error(request," esta cuenta ya esta registrada pero nadie la administra aun")
				else:
					cb = CUENTA_BANCARIA()
					cb.banco = banco
					cb.tienda = us 
					cb.numero_de_cuenta = numero
					cb.capital =monto
					cb.save()

					messages.success(request," fue creado satisfactoriamente")
			context ={
				"form":form,
				"tienda":us
			}
			return render(request, self.template_name, context)
		return redirect("/")

		


class menu_bancario(TemplateView):
	template_name="bancos/menu.html"
	def get(self,request,*args,**kwargs):
		if OKadmin(request):
			context={
				"HOLA":"adios"
			}
			return render(request,self.template_name,context)
		return redirect("/")

class crear_banco(TemplateView):
	template_name="bancos/crear.html"
	forms = BancoForm
	initial = {'key': 'value'}
	def get(self,request,*args,**kwargs):
		if OKadmin(request):
			form = self.forms(initial=self.initial)
			context={
				"form":form
			}
			return render(request,self.template_name,context)
		return redirect("/")
	def post(self,request,*args,**kwargs):
		if OKadmin(request):
			form = self.forms(request.POST)
			if form.is_valid():
				f=form.cleaned_data['banco']
				f=f.upper()
				banco = BANCO.objects.filter(nombre=f)
				if banco.exists():
					messages.error(request,"este banco ya existe")
				else:
					b = BANCO()
					b.nombre=f
					b.save()
					messages.success(request,f+" fue creado satisfactoriamente")
			context ={
				"form":form,
			}
			return render(request, self.template_name, context)
		return redirect("/")

