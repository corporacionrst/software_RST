# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from ....request_session import OKcobros,getPerfil
from .models import CONTRASENA
from ....productos.inventario.orden.models import ORDEN_DE_COMPRA
# Create your views here.
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from .models import CONTRASENA_ACTUAL,CONTRASENA
from ....productos.inventario.historial.models import HISTORIAL
from ....cliente_proveedor.proveedor.models import PROVEEDOR

from datetime import date, timedelta

import datetime

class quitar_contrasena(TemplateView):
	def post(self,request,*args,**kwargs):
		if OKcobros(request):
			val = request.POST['documento']
			tienda = getPerfil(request).tienda
			odc = ORDEN_DE_COMPRA.objects.get(id=val)
			pr=odc.proveedor
			oc_numero=odc.documento
			oc_numero.documento=""
			oc_numero.save()
			oc_lista=odc.lista
			oc_lista.tipo_doc="O"
			oc_lista.save()
			oc = ORDEN_DE_COMPRA.objects.get(id=val)
			oc.doc_contra=None
			oc.save()
			return HttpResponse("+",content_type='text')
		return HttpResponse("no tienes permiso para manipular este tipo de documentos",content_type='text')
			





		

class cargar_a_contrasena(TemplateView):
	def post(self,request,*args,**kwargs):
		if OKcobros(request):
			val = request.POST['documento']
			numero=str(request.POST['numero']).upper()
			serie = str(request.POST['serie']).upper()
			tienda = getPerfil(request).tienda
			odc = ORDEN_DE_COMPRA.objects.get(id=val)
			his = HISTORIAL.objects.filter(documento=numero).filter(lista__tipo_doc="C").filter(cliente_proveedor=odc.proveedor.info).filter(serie=serie)
			if not his.exists() and numero!="" and serie!="":
				pr=odc.proveedor
				oc_numero=odc.documento
				oc_numero.documento=numero
				oc_numero.serie=serie
				oc_numero.save()
				oc_lista=odc.lista
				oc_lista.tipo_doc="C"
				oc_lista.save()
				c_actual=CONTRASENA_ACTUAL.objects.filter(proveedor=pr).filter(tienda=tienda)
				if c_actual.exists():
					contrasena = CONTRASENA.objects.filter(ubicado=c_actual[0]).filter(correlativo=c_actual[0].actual)
					if contrasena.exists():
						contrasena=contrasena[0]
					else:
						contrasena=CONTRASENA()
						contrasena.ubicado=c_actual[0]
						contrasena.correlativo=c_actual[0].actual
						contrasena.total=0
					contrasena.total=contrasena.total+odc.lista.total
					contrasena.fehca_registro=datetime.datetime.now()
					contrasena.save()
					if odc.doc_contra==None:
						odc.doc_contra=contrasena
					
				else:
					c_actual=CONTRASENA_ACTUAL()
					c_actual.proveedor=odc.proveedor
					c_actual.tienda=tienda
					c_actual.actual=1
					c_actual.save()
					contrasena=CONTRASENA()
					contrasena.ubicado=c_actual
					contrasena.correlativo=1
					contrasena.total=odc.lista.total
					contrasena.fehca_registro=datetime.datetime.now()
					contrasena.save()
					odc.doc_contra=contrasena
				odc.save()
				return HttpResponse("+",content_type='text')
			return HttpResponse("el documento fue registrado por '"+his[0].ingresa.usuario.username+"' en la fecha "+str(his[0].fehca_registro)+", favor revisar",content_type='text')
		return HttpResponse("no tienes permiso para manipular este tipo de documentos",content_type='text')
			


class lista_contrasena(TemplateView):
	template_name="sistema/cobros/lista_contrasenas.html"
	def get(self,request,*args,**kwargs):
		if OKcobros(request):
			us = getPerfil(request)
			context={
				"tienda":us.tienda
			}
			return render(request,self.template_name,context)

		else:
			return redirect("/")

class por_nit_contrasena(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKcobros(request):
			nit = request.GET['nit']
			us = getPerfil(request)
			odc = ORDEN_DE_COMPRA.objects.filter(proveedor__info__nit=nit).filter(doc_contra__isnull=True).filter(autorizada=True).filter(lista__credito=True)[0:10]
			odc=odc.values("proveedor__info__nit","proveedor__info__nombre","id","lista__total")
			odc=json.dumps(list(odc),cls=DjangoJSONEncoder)
			return HttpResponse(odc,content_type='application/json')
		return HttpResponse("{}",content_type='application/json')
		


class lista_de_contrasena(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKcobros(request):
			nit = request.GET['nit']
			pr = PROVEEDOR.objects.filter(info=nit)
			tienda= getPerfil(request).tienda
			if pr.exists():
				prv=pr[0]
				actual=CONTRASENA_ACTUAL.objects.filter(tienda=tienda).filter(proveedor__info__nit=prv.info.nit)
				if actual.exists():
					passwd = CONTRASENA.objects.filter(ubicado=actual[0]).filter(correlativo=actual[0].actual)
					if passwd.exists():
						odc = ORDEN_DE_COMPRA.objects.filter(doc_contra=passwd[0]).values("id","documento__documento","lista__total","documento__serie")
						odc=json.dumps(list(odc),cls=DjangoJSONEncoder)
						return HttpResponse(odc,content_type='application/json')
					
		return HttpResponse("{}",content_type='application/json')

class showpasswd(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKcobros(request):
			nit = request.GET['nit']
			c_actual=request.GET['actual']
			pr = PROVEEDOR.objects.filter(info=nit)
			tienda= getPerfil(request).tienda
			if pr.exists():
				prv=pr[0]
				actual=CONTRASENA_ACTUAL.objects.filter(tienda=tienda).filter(proveedor__info__nit=prv.info.nit)
				if actual.exists():
					passwd = CONTRASENA.objects.get(no=c_actual)
					odc = ORDEN_DE_COMPRA.objects.filter(doc_contra=passwd).values("documento__documento","documento__serie","fecha_registro","lista__total")
					odc=json.dumps(list(odc),cls=DjangoJSONEncoder)
					return HttpResponse(odc,content_type='application/json')
					
		return HttpResponse("{}",content_type='application/json')




class imprimir_contrasena(TemplateView):
	def post(self,request,*args,**kwargs):
		if OKcobros(request):
			nit = request.POST['nit']
			pr = PROVEEDOR.objects.filter(info=nit)
			tienda= getPerfil(request).tienda
			if pr.exists():
				prv=pr[0]
				actual=CONTRASENA_ACTUAL.objects.filter(tienda=tienda).filter(proveedor__info__nit=prv.info.nit)
				if actual.exists():
					con = CONTRASENA.objects.filter(ubicado=actual[0]).filter(correlativo=actual[0].actual)
					if con.exists():
						prv.monto=prv.monto+con[0].total
						prv.save()
						c_actual=actual[0]
						retorno=c_actual.actual
						c_actual.actual=retorno+1
						c_actual.save()
						return HttpResponse(retorno,content_type='text')
		return HttpResponse("-1",content_type='text')
	def get(self,request,*args,**kwargs):
		if OKcobros(request):
			nit = request.GET['nit']
			pr = PROVEEDOR.objects.filter(info=nit)
			tienda= getPerfil(request).tienda
			if pr.exists():
				prv=pr[0]
				actual=CONTRASENA_ACTUAL.objects.filter(tienda=tienda).filter(proveedor__info__nit=prv.info.nit)
				if actual.exists():
					con = CONTRASENA.objects.filter(ubicado=actual[0]).filter(correlativo=actual[0].actual)
					if con.exists():
						return HttpResponse(con[0].no,content_type='text')
		return HttpResponse("-1",content_type='text')

class contrasena_impresa(TemplateView):
	template_name="impresion/contrasena.html"
	def get(self,request,id=None,*args,**kwargs):
		actual = CONTRASENA_ACTUAL.objects.filter()
		contrasena= CONTRASENA.objects.filter(no=id)
		if contrasena.exists():
			bus=contrasena[0].ubicado.tienda
			name=bus.nombre
			addr=bus.direccion
			phone = bus.telefono
			fecha = contrasena[0].fehca_registro
			dias = contrasena[0].ubicado.proveedor.dias_credito
			pago = fecha+timedelta(days=dias)
			comunicado="contraseña generada por '"+name+"', solicitud de su pago en aproximadamente '"+str(dias)+"' dias despues de la emision del siguiente documento"
			nit= bus.nit
			context={
				"nombre_empresa":name,
				"addr":addr,
				"nit_E":nit,
				"tipo":"CONTRASEÑA",
				"telefono":"PBX:"+phone,
				"numero":contrasena[0].no,
				"fecha":fecha,
				"nit":contrasena[0].ubicado.proveedor.info.nit,
				"nombre":contrasena[0].ubicado.proveedor.info.nombre,
				"direccion":contrasena[0].ubicado.proveedor.info.direccion,
				"credito":"CREDITO",
				"comunicado":comunicado,
				"total_documento":contrasena[0].total,
				"pago": pago
			}
			return render(request,self.template_name,context)
		return redirect("/caja/contrasenas/")
