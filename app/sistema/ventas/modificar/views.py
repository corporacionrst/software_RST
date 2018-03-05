# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect

from ....productos.inventario.forms import *
from ....request_session import *

# Create your views here.
from django.views.generic import TemplateView

class menu(TemplateView):
	template_view="facturacion/modificar/menu/"
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			pl = self.template_name+obtenerPlantilla(request)
			usu = getPerfil(request)
			context={
				"tienda":usu.tienda
			}
			return render(request,pl,context)
		return redirect("/")

class modificar(TemplateView):
	template_name="facturacion/facturas/"
	formU = FormPersona
	url = "/clientes/nit"
	initial={'key':'value'}
	formulario=Form_registrar
	def get(self,request,id=None,*args,**kwargs):
		indice=int(id)
		if indice<5 and indice>0:
			if  OKpeople(request):
				plantilla=self.template_name+obtenerPlantilla(request)
				usu= getPerfil(request)
				ut = USUARIO_TIENDA.objects.filter(usuario=usu).filter(tienda=usu.tienda)
				if ut.exists():
					ut=ut[0]
					correlativo=None
					if indice==1:
						correlativo=ut.fac_1
					elif indice==2:
						correlativo=ut.fac_2
					elif indice==3:
						correlativo=ut.fac_3
					else:
						correlativo=ut.fac_4	
					dpt=DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=indice).filter(correlativo=correlativo).filter(tipo_doc="V")
					if not dpt.exists():
						dpt=DOCUMENTO_POR_TIENDA()
						dpt.ubicado=ut
						dpt.pagina=indice
						dpt.correlativo=correlativo
						dpt.save()
				tienda=usu.tienda
				form=self.formU(initial=self.initial)
				fm = self.formulario(initial=self.initial)
				context={
				"tienda":tienda.nombre,
				"store":tienda.id,
				"form":form,
				"formulario":fm,
				"url":self.url,
				"accion":"Facturar",
				"pagina":indice
				}
				return render(request, plantilla, context)

		return redirect("/")
