# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from ....request_session import OKcobros,getPerfil
from ....productos.inventario.orden.models import ORDEN_DE_COMPRA
from ..cobro.models import DOCUMENTOS_POR_CAJA
# Create your views here.
from django.db.models import Q

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

from ....productos.inventario.historial.models import *
from ....cliente_proveedor.cliente.models import CLIENTE
from ....bancos.cuentas_por_cobrar.models import DOCUMENTO_POR_COBRAR

from .tasks import descargar_de_inventario
import datetime
from datetime import date, timedelta

from channels import Channel

class imprimir(TemplateView):
	template_name="impresion/documento.html"
	def post(self,request,*args,**kwargs):
		if OKcobros(request):
			serie=request.POST["serie"]
			documento = request.POST["documento"]
			dpcaja =DOCUMENTOS_POR_CAJA.objects.get(id=serie)
			his = HISTORIAL.objects.get(id=documento)
			his.serie=dpcaja.serie
			his.fehca_registro=datetime.datetime.today()
			dia=date.today()
			if dia.day>=20 and dia.day<=26:
				fin_mes=datetime.date(dia.year,dia.month+1,1)-timedelta(days=1)
				dia=date.today()+timedelta(days=(fin_mes.day+1)-date.today().day)
			else:
				dia=dia+timedelta(days=5)
			dpc=DOCUMENTO_POR_COBRAR()
			dpc.documento=his
			cliente = CLIENTE.objects.filter(info=his.cliente_proveedor).filter(store=his.lista.ubicado.tienda)[0]
			if his.lista.credito:
				if cliente.credito and cliente.saldo<cliente.monto:
					dpc.fecha_limite=date.today()+timedelta(cliente.dias_credito)
				else:
					return HttpResponse("***venta unicamente por CONTADO***",content_type='text')
			else:
				dpc.fecha_limite=date.today()
			if his.lista.descuento>0:
				dpc.pendiente=his.lista.descuento
			else:
				dpc.pendiente=his.lista.total

			c_infile = CORRELATIVO_INFILE()
			c_infile.serie =dpcaja
			c_infile.documento =his
			c_infile.fecha_creacion=date.today()
			c_infile.fecha_a_registrar=dia
			
			task_id=descargar_de_inventario.delay(his.lista.id)
			c_infile.save()
			dpc.save()
			mail=his.cliente_proveedor.correo
			his.save()
			return HttpResponse(mail,content_type="text")

		return HttpResponse("***no tienes autorizada esta funcion***",content_type='text')
		


class factura(TemplateView):
	template_name="impresion/documento.html"
	def get(self,request,id=None,*args,**kwargs):
		if OKcobros(request):
			his = HISTORIAL.objects.get(id=id)
			name = his.lista.ubicado.tienda.nombre
			paginas = LISTA_PRODUCTO.objects.filter(lista=his.lista).count()/10
			bus=his.lista.ubicado.tienda
			name=bus.nombre
			addr=bus.direccion
			phone = bus.telefono
			nit= bus.nit
			cliente = CLIENTE.objects.filter(info=his.cliente_proveedor).filter(store=his.lista.ubicado.tienda)[0]
			comunicado="El siguiente documento es un comprobante de que la empresa '"+name+"' "
			comunicado+="despacho la mercadería listada anteriormente.La factura original sera enviada al "
			comunicado+="correo '"+cliente.info.correo+"' en un estimado de 5 a 8 dias "
			comunicado+="despues de emitido este documento dependiendo de su fecha de "
			comunicado+="emision, despues de esa fecha, no se aceptará ningún tipo de reclamo, cambio o devolución"
			if his.lista.credito:
				credito="CREDITO"
			else:
				credito="CONTADO"
			context={
				"nombre_empresa":name,
				"addr":addr,
				"nit_E":nit,
				"tipo":"DOCUMENTO DE COMPRA",
				"telefono":"PBX:"+phone,
				"numero":his.serie+":"+str(his.id),
				"fecha":his.fehca_registro,
				"nit":cliente.info.nit,
				"nombre":cliente.info.nombre,
				"direccion":cliente.info.direccion,
				"credito":credito,
				"solicitud":"vendedor",
				"usuario":his.lista.ubicado.usuario.usuario.id,
				"paginas":paginas,
				"lista":his.lista,
				"comunicado":comunicado,
				"total_documento":his.lista.total
			}
			return render(request,self.template_name,context)

		return redirect("/")


class contado(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKcobros(request):
			pag=int(request.GET['pag'])
			usu=getPerfil(request)
			his = HISTORIAL.objects.filter(lista__tipo_doc="V").filter(serie="").filter(documento="").filter(lista__ubicado__tienda=usu.tienda).filter(lista__credito=False)[pag:pag+10]
			his=his.values("id","cliente_proveedor__nit","cliente_proveedor__nombre","lista__total","lista__descuento")
			his=json.dumps(list(his),cls=DjangoJSONEncoder)
			return HttpResponse(his,content_type='application/json')
		return HttpResponse("{}",content_type='application/json')
		

class credito(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKcobros(request):
			pag=int(request.GET['pag'])
			usu=getPerfil(request)
			his = HISTORIAL.objects.filter(lista__tipo_doc="V").filter(serie="").filter(documento="").filter(lista__ubicado__tienda=usu.tienda).filter(lista__credito=True)[pag:pag+10]
			his=his.values("id","cliente_proveedor__nit","cliente_proveedor__nombre","lista__total","lista__descuento")
			his=json.dumps(list(his),cls=DjangoJSONEncoder)
			return HttpResponse(his,content_type='application/json')
		return HttpResponse("{}",content_type='application/json')
		
class cola(TemplateView):
	template_name="sistema/cobros/cola.html"
	def get(self,request,*args,**kwargs):
		if OKcobros(request):
			usu = getPerfil(request)
			serie=DOCUMENTOS_POR_CAJA.objects.filter(tienda=usu.tienda).filter(usuario=usu)
			context={
			"tienda":usu.tienda,
			"serie":serie
			}
			return render(request,self.template_name,context)

		return redirect("/")
		

class menu_cobros(TemplateView):
	template_name="sistema/cobros/index.html"
	def get(self,request,*args,**kwargs):
		if OKcobros(request):
			usu = getPerfil(request)
			contra = ORDEN_DE_COMPRA.objects.filter(lista__ubicado__tienda=usu.tienda).filter(doc_contra__isnull=True).filter(lista__credito=True).count()
			cola = HISTORIAL.objects.filter(lista__tipo_doc="V").filter(serie="").filter(documento="").filter(lista__ubicado__tienda=usu.tienda).count()
			cobros="X"
			contex={
				"cola":cola,
				"passwd":contra,
				"cobros":cobros
			}
			return render(request,self.template_name,contex)	
		return redirect("/")
	def post(self,request,*args,**kwargs):
		if OKcobros(request):
			# serie=request.POST["serie"]
			# documento = request.POST["documento"]
			
			# dpc =DOCUMENTOS_POR_CAJA.objects.get(id=serie)
			# his = HISTORIAL.objects.get(id=documento)
			# his.serie=dpc.serie
			# his.fehca_registro=datetime.datetime.today()
			# dia=date.today()
			# if dia.day>=20 and dia.day<=26:
			# 	fin_mes=datetime.date(dia.year,dia.month+1,1)-timedelta(days=1)
			# 	dia=date.today()+timedelta(days=(fin_mes.day+1)-date.today().day)
			# else:
			# 	dia=dia+timedelta(days=5)
			# ci=CORRELATIVO_INFILE()
			# ci.serie = dpc
			# ci.documento = his
			# ci.fecha_creacion=date.today()
			# ci.fecha_a_registrar=dia
			# ci.save()
			# mail=his.cliente_proveedor.correo
			# his.save()
			# return HttpResponse(mail,content_type="text")
			print ":)"

		return HttpResponse("***no tienes autorizada esta funcion***",content_type='text')



			
