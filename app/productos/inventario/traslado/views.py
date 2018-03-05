# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from ....sistema.usuarios.models import Perfil
from ....request_session import getPerfil,OKbodega

# Create your views here.
class traslados(TemplateView):
	template_view = "productos/traslados/traslados.html"
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			context={
				"hola":"adios",
				"tienda":getPerfil(request).tienda
			}
			return render(request,self.template_view,context)
		return redirect("/")

class autorizar_traslados(TemplateView):
	template_view="productos/traslados/autorizar.html"
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			usu=getPerfil(request)
			context={
				"tienda":usu.tienda
			}
			return render(request,self.template_view,context)
		return redirect("/")