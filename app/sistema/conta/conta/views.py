# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from ....request_session import OKconta,getPerfil
from ...usuarios.models import Perfil
from ...tienda.models import EMPRESA

from ...cobros.cobro.models import DOCUMENTOS_POR_CAJA

from django.views.generic import TemplateView
from django.db.models import Q

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

from .forms import FormDocumento

# Create your views here.
class usuarios_por_tienda(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKconta(request):
			tienda = request.GET["tienda"]
			store = EMPRESA.objects.get(id=tienda)
			t = Perfil.objects.filter(tienda=store).filter(Q(puesto__nombre__icontains="admin")|Q(puesto__nombre__icontains="cobro")).values("id","usuario__username","puesto__nombre")
			t=json.dumps(list(t),cls=DjangoJSONEncoder)
			return HttpResponse(t,content_type='application/json')
		return HttpResponse("{}",content_type="application/json")

class documentos(TemplateView):
	template_name="sistema/conta/documentos.html"
	doc_form = FormDocumento
	initial={'key':'value'}
	def get(self,request,*args,**kwargs):
		if OKconta(request):
			tienda = EMPRESA.objects.all()
			usu = getPerfil(request)
			form = self.doc_form(initial=self.initial)
			context={
			"tienda":tienda,
			"form":form
			}
			return render(request,self.template_name,context)
		return redirect("/")
	def post(self,request,*args,**kwargs):
		if OKconta(request):
			valor = request.POST['usuario']
			tienda = EMPRESA.objects.all()
			form = self.doc_form(request.POST or None)
			if form.is_valid() and  valor!="":
				valor=int(valor)
				tienda= form.cleaned_data['tienda']
				serie= str(form.cleaned_data['serie']).upper()
				documento=form.cleaned_data['documento']
				if documento==None:
					documento=1
				usu = Perfil.objects.get(id=valor)
				dpc= DOCUMENTOS_POR_CAJA.objects.filter(tienda=tienda).filter(usuario=usu).filter(serie=serie)
				if not dpc.exists():
					dpc= DOCUMENTOS_POR_CAJA()
					dpc.tienda=tienda
					dpc.usuario=usu
					dpc.serie=serie
					dpc.correlativo=documento
					dpc.save()
					return HttpResponse("V",content_type='text')
				else:
					dpc=dpc[0]
					return HttpResponse("este documento ya existe, y va por el valor "+str(dpc.correlativo),content_type='text')
			else:
				return HttpResponse("por favor llene todas las casillas",content_type='text')	
		return HttpResponse("no tienes permiso para efectuar esta operacion",content_type='text')
				




class conta(TemplateView):
	template_name="sistema/conta/index.html"
	def get(self,request,*args,**kwargs):
		if OKconta(request):
			context={
				"hola":"adios"
			}
			return render(request,self.template_name,context)

		return redirect("/")
