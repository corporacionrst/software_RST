# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView

from django.http import HttpResponse
from .models import *
from ..request_session import *

from django.core.serializers.json import DjangoJSONEncoder
import json

# Create your views here.

class bell(TemplateView):
	def get(self,request,*args,**kwargs):
		perfil = getPerfil(request)
		alerta = ALERTA.objects.filter(puesto=perfil.puesto).filter(tienda=perfil.tienda).filter(tipo=0).filter(visto=False)[0:5]
		if alerta.exists():
			alerta=alerta.values("mensaje","sub_mensaje","requiere__usuario__username","ruta","tipo","puesto__nombre")
			alerta= json.dumps(list(alerta),cls=DjangoJSONEncoder)
			return HttpResponse(alerta,content_type='application/json')
		else:
			return HttpResponse("{}",content_type='application/json')

class notify(TemplateView):
	def get(self,request,*args,**kwargs):
		perfil = getPerfil(request)
		alerta = ALERTA.objects.filter(puesto=perfil.puesto).filter(tienda=perfil.tienda).filter(tipo=1).filter(visto=False)[0:5]
		if alerta.exists():
			alerta=alerta.values("mensaje","sub_mensaje","requiere__usuario__username","ruta","tipo")
			alerta= json.dumps(list(alerta),cls=DjangoJSONEncoder)
			return HttpResponse(alerta,content_type='application/json')
		else:
			return HttpResponse("{}",content_type='application/json')

class dispatch(TemplateView):
	def get(self,request,*args,**kwargs):
		perfil = getPerfil(request)
		alerta = ALERTA.objects.filter(puesto=perfil.puesto).filter(tienda=perfil.tienda)[0:5]
		if alerta.exists():
			alerta=alerta.values("mensaje","sub_mensaje","requiere__usuario__username","ruta")
			alerta= json.dumps(list(alerta),cls=DjangoJSONEncoder)
			return HttpResponse(alerta,content_type='application/json')
		else:
			return HttpResponse("{}",content_type='application/json')




class arranque_alertas(TemplateView):
	def get(self,request,*args,**kwargs):
		perfil = getPerfil(request)
		alerta = ALERTA.objects.filter(puesto=perfil.puesto)[0:5]
		if alerta.exists():
			alerta=alerta.values("mensaje","sub_mensaje","requiere__usuario__username","ruta")
			alerta= json.dumps(list(alerta),cls=DjangoJSONEncoder)
			return HttpResponse(alerta,content_type='application/json')
		else:
			print "esto"
			return HttpResponse("{}",content_type='application/json')


