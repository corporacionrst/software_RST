# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from ....request_session import getPerfil, OKcobros
from ....bancos.banco.models import CUENTA_BANCARIA
from .tasks import realizar_deposito_cuentas,descartar_deposito_cuentas,autorizar_deposito_cuentas

from django.contrib import messages
# Create your views here.

from django.http import HttpResponse
from .models import DEPOSITOS

from django.core.serializers.json import DjangoJSONEncoder
import json

class cola_depositos(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKcobros(request):
			pag = int(request.GET['pag'])*5
			pr = getPerfil(request)
			oc = DEPOSITOS.objects.filter(cuenta_acreditada__administra=pr).filter(visto=False)[pag:pag+5]
			oc=oc.values("cuenta_debitada__banco","cuenta_debitada__administra__usuario__username","cuenta_debitada__numero_de_cuenta","cuenta_acreditada__numero_de_cuenta","monto","visto","confirmar","id","monto","documento")
			oc=json.dumps(list(oc),cls=DjangoJSONEncoder)
			return HttpResponse(oc,content_type='application/json')
		return HttpResponse("{}",content_type='application/json')


class confirmar_depositos(TemplateView):
	template_name="sistema/cobros/confirmar.html"
	def get(self,request,*args,**kwargs):
		if OKcobros(request):
			pr = getPerfil(request)
			
			return render(request,self.template_name,{"tienda":pr.tienda})

		return redirect("/")



class hacer_depositos(TemplateView):
	template_name= "sistema/cobros/depositos.html"
	def get(self, request ,*args, **kwargs):
		if OKcobros(request):
			usuario = getPerfil(request)
			de = CUENTA_BANCARIA.objects.filter(administra=usuario).filter(tienda=usuario.tienda)
			para = CUENTA_BANCARIA.objects.filter(tienda=usuario.tienda)
			context={
				"de":de,
				"para":para,
				"tienda":usuario.tienda
			}
			return render(request,self.template_name,context)
		return redirect("/")
	def post(self,request,*args,**kwargs):
		return redirect("/caja/depositos/")





def realizar_deposito(de,para,monto,documento,reply_channel):
	task_id = realizar_deposito_cuentas.delay(de,para,monto,documento,reply_channel)


def descartar_deposito_de_cuentas(no,reply_channel):
	task_id = descartar_deposito_cuentas.delay(no,reply_channel)



def autorizar_deposito_de_cuenta(no,reply_channel):
	task_id= autorizar_deposito_cuentas.delay(no,reply_channel)

