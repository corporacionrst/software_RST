# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect

from ..request_session import OKpeople,getPerfil,obtenerPlantilla,OKadmin
from django.views.generic import TemplateView

from django.http import HttpResponse

from ..productos.producto.models import PRODUCTO
from ..sistema.usuarios.models import USUARIO_TIENDA,DOCUMENTO_POR_TIENDA
from ..productos.inventario.inventario.models import INVENTARIO
from ..productos.inventario.historial.models import LISTA_PRODUCTO
from .models import PROFORMA
from decimal import Decimal

from datetime import date, datetime,timedelta
import json
from django.core.serializers.json import DjangoJSONEncoder

from ..productos.inventario.forms import *
from ..cliente_proveedor.persona.models import PERSONA
from ..productos.inventario.historial.models import HISTORIAL

from datetime import date, datetime


import datetime

class vincular_pr(TemplateView):
	template_name="productos/proforma/imprimir/"
	formU = FormPersona
	url = "/clientes/nit"
	initial={'key':'value'}
	formulario=Form_registrar
	def get(self,request,id=None,*args,**kwargs):
		if OKpeople(request):
			indice=int(id)
			proforma = PROFORMA.objects.get(id=id)
			fecha = proforma.fecha_vencimiento-date.today()
			plantilla=self.template_name+obtenerPlantilla(request)
			form=self.formU(initial=self.initial)
			fm = self.formulario(initial=self.initial)
			info =LISTA_PRODUCTO.objects.filter(lista=proforma.lista)
			if fecha.days>0:
				context={
					"tienda":proforma.lista.ubicado.tienda,
					"numero":id,
					"form":form,
					"formulario":fm,
					"info":info,
					"total":proforma.lista.total
				
				}
				return render(request,plantilla,context)
		return redirect("/")
	def post(self,request,*args,**kwargs):
		if OKpeople(request):
			nit=str(request.POST["nit"]).upper()
			credito=request.POST["credito"]
			pag=request.POST["proforma"]
			proforma=PROFORMA.objects.get(id=pag)
			if (proforma.fecha_vencimiento-date.today()).days>=0:
				registra=proforma.lista.ubicado.usuario
				ut =USUARIO_TIENDA.objects.filter(usuario=registra).filter(tienda=proforma.lista.ubicado.tienda)
				if ut.exists() :
					dpt = proforma.lista
					mensaje="documento en caja"
					if "true" in credito:
						dpt.credito=True
						dpt.save()
					cp = PERSONA.objects.get(nit=nit)
					try:
						h = HISTORIAL()
						h.cliente_proveedor=cp
						h.fehca_registro=datetime.datetime.now()
						h.ingresa=registra
						h.lista=dpt
						dpt.tipo_doc="V"
						h.save()
						dpt.save()
					except:
						return HttpResponse("Esta proforma ya fue previamente registrada",content_type='text')
					return HttpResponse("Documento en caja",content_type='text')
				return HttpResponse("hubo problemas con identificar el usuario/tienda",content_type="text")
			return HttpResponse("Esta proforma ha caducado",content_type='text')
		return HttpResponse("no tienes permisos para registrar una compra",content_type='text')












class proforma(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			pag=int(request.GET['pag'])*10
			usu=getPerfil(request)
			his = PROFORMA.objects.filter(lista__tipo_doc="P").filter(lista__ubicado__tienda=usu.tienda).filter(fecha_vencimiento__gte=date.today()).order_by("-fecha_vencimiento")[pag:pag+10]
			his=his.values("id","vendedor__usuario__username","vendedor__usuario__id","fecha_vencimiento")
			his=json.dumps(list(his),cls=DjangoJSONEncoder)
			return HttpResponse(his,content_type='application/json')
		return HttpResponse("{}",content_type='application/json')

class buscarProforma(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			pag=int(request.GET['numero'])*10
			usu=getPerfil(request)
			his = PROFORMA.objects.filter(id__contains=pag).filter(lista__ubicado__tienda=usu.tienda).filter(fecha_vencimiento__gte=date.today())[pag:pag+10]
			his=his.values("id","vendedor__usuario__username","vendedor__usuario__id")
			his=json.dumps(list(his),cls=DjangoJSONEncoder)
			return HttpResponse(his,content_type='application/json')
		return HttpResponse("{}",content_type='application/json')



class vincular(TemplateView):
	template_name="productos/proforma/vincular/"
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			usu=getPerfil(request)
			context={
				"tienda":usu.tienda
			}
			pl = self.template_name+obtenerPlantilla(request)
			return render(request,pl,context)
		return redirect("/")





class imprimir(TemplateView):
	def post(self,request,*args,**kwargs):
		mensaje="la lista parece estar vacia"
		if OKpeople(request):
			cliente =request.POST['cliente']
			telefono = request.POST['telefono']
			correo= request.POST['correo']
			usu = getPerfil(request)
			ut = USUARIO_TIENDA.objects.filter(usuario=usu).filter(tienda=usu.tienda)
			if ut.exists():
				ut=ut[0]
				dpt = DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=5).filter(correlativo=ut.proforma).filter(tipo_doc="P")
				if dpt.exists():
					lp=LISTA_PRODUCTO.objects.filter(lista=dpt).count()
					if lp>0:
						dpt=dpt[0]
						ut.proforma=int(ut.proforma)+1
						pr = PROFORMA()
						pr.atencion= cliente
						pr.telefono=telefono
						pr.correo=correo

						pr.fehca_registro = date.today()
						pr.fecha_vencimiento = date.today()+timedelta(days=7)
						pr.vendedor=usu
						pr.lista=dpt
						pr.save()
						ut.save()
						mensaje=pr.id

		return HttpResponse(mensaje,content_type="text");



class quitar_prod_factura(TemplateView):
	def post(self,request,*args,**kwargs):
		if OKpeople(request):
			usu = getPerfil(request)
			ut = USUARIO_TIENDA.objects.filter(usuario=usu).filter(tienda=usu.tienda)
			if ut.exists():
				ut=ut[0]
				dpt = DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=5).filter(correlativo=ut.proforma).filter(tipo_doc="P")
				if dpt.exists():
					dpt=dpt[0]
					try:
						producto =request.POST['producto']
						prod = PRODUCTO.objects.get(id=producto)
						lp=LISTA_PRODUCTO.objects.filter(lista=dpt).filter(producto=prod)
						if  lp.exists():
							dpt.total=dpt.total-(Decimal(lp[0].cantidad)*Decimal(lp[0].unitario))
							dpt.save()
							lp[0].delete()
							message="eliminado"
							return HttpResponse(message,content_type='text')
					except:
						return HttpResponse("el producto no existe,favor reportar este error inmediatamente",content_type='text')
		return HttpResponse("no se encontro elemento para borrar",content_type='text')





class total_venta(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			usu = getPerfil(request)
			ut = USUARIO_TIENDA.objects.filter(usuario=usu).filter(tienda=usu.tienda)
			if ut.exists():
				ut=ut[0]
				dpt=DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=5).filter(correlativo=ut.proforma).filter(tipo_doc="P")
				if dpt.exists():
					dpt=dpt[0]
					total=dpt.total
					return HttpResponse(total,content_type="text")

		return HttpResponse("0",content_type="text")




class cargar_a_lista_factura(TemplateView):
	def post(self,request,*args,**kwargs):
		message="{}"
		if OKpeople(request):
			cantidad=request.POST['cantidad']
			if cantidad!="":
				producto =request.POST['producto']
				prod = PRODUCTO.objects.get(id=producto)
				cantidad =int(cantidad)
				precio   =request.POST['precio']
				usu = getPerfil(request)
				ut = USUARIO_TIENDA.objects.filter(usuario=usu).filter(tienda=usu.tienda)
				if ut.exists():
					ut=ut[0]
					dpt=DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=5).filter(correlativo=ut.proforma).filter(tipo_doc="P")
					if dpt.exists():
						dpt=dpt[0]
						INV= INVENTARIO.objects.filter(tienda=usu.tienda).filter(producto=prod)
						if INV.exists():
							INV=INV[0]
							if precio=="":
								precio = Decimal(INV.tarjeta)
							if INV.cantidad>=cantidad:
								if Decimal(INV.efectivo)<=Decimal(precio):
									lp = LISTA_PRODUCTO.objects.filter(lista=dpt).filter(producto=prod)
									if lp.exists():
										message="este elemento ya fue agregado previamente"
									else:
										lp=LISTA_PRODUCTO()
										lp.lista=dpt
										lp.producto=prod
										lp.cantidad=int(cantidad)
										lp.unitario=Decimal(precio)
										lp.tipo_doc="P"
										lp.save()
										dpt.total=dpt.total+(Decimal(cantidad)*Decimal(precio))
										dpt.save()
										message="agregado correctamente"
								else:
									message="el precio es demasiado bajo"
							else:
								message="no hay productos suficientes en esta tienda"
					else:
						INV= INVENTARIO.objects.filter(tienda=usu.tienda).filter(producto=prod)
						if INV.exists():
							INV=INV[0]
							if precio=="":
								precio = Decimal(INV.tarjeta)
							if INV.cantidad>=cantidad:
								dpt=DOCUMENTO_POR_TIENDA()
								dpt.ubicado=ut
								dpt.pagina=5
								dpt.correlativo=ut.proforma
								dpt.save()
								lp=LISTA_PRODUCTO()
								lp.lista=dpt
								lp.producto=prod
								lp.cantidad=int(cantidad)
								lp.unitario=Decimal(precio)
								lp.tipo_doc="P"
								lp.save()
								dpt.total=Decimal(cantidad)*Decimal(precio)
								dpt.save()
								message="agregado correctamente"
							else:
								message="la cantidad no es valida"
						else:
							message="error con el inventario, favor reportarlo de inmediato"
				else:
					ut=USUARIO_TIENDA()
					ut.usuario=usu
					ut.tienda=usu.tienda
					ut.save()
					dpt=DOCUMENTO_POR_TIENDA()
					dpt.ubicado=ut
					dpt.pagina=pag
					dpt.save()
					lp=LISTA_PRODUCTO()
					lp.lista=dpt
					lp.producto=prod
					lp.cantidad=int(cantidad)
					lp.unitario=Decimal(precio)
					lp.save()
					dpt.total=Decimal(cantidad)*Decimal(precio)
					dpt.save()
					message="agregado correctamente"
			else:
				message="la cantidad parece estar vacia"

		return HttpResponse(message,content_type='text')



class listar_datos_factura(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			perfil = getPerfil(request)
			ut = USUARIO_TIENDA.objects.filter(usuario=perfil).filter(tienda=perfil.tienda)
			if ut.exists():
				ut=ut[0]
				dpt =DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=5).filter(correlativo=ut.proforma).filter(tipo_doc="P")
				if dpt.exists():
					dpt=dpt[0]
					i=int(request.GET["pag"])*5
					Lista=LISTA_PRODUCTO.objects.filter(lista=dpt).values("producto__codigo","producto__descripcion","producto__marca","cantidad","unitario","producto__id").order_by("producto__codigo")[i:i+5]
					Lista=json.dumps(list(Lista),cls=DjangoJSONEncoder)
					return HttpResponse(Lista,content_type="application/json")
				
		return HttpResponse("{}",content_type="application/json")
			


class generar(TemplateView):
	template_name="productos/proforma/generar/"
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			plantilla=self.template_name+obtenerPlantilla(request)
			usu= getPerfil(request)
			ut = USUARIO_TIENDA.objects.filter(usuario=usu).filter(tienda=usu.tienda)
			if ut.exists():
				ut=ut[0]
				dpt=DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=5).filter(correlativo=ut.proforma).filter(tipo_doc="P")
				if not dpt.exists():
					dpt=DOCUMENTO_POR_TIENDA()
					dpt.ubicado=ut
					dpt.pagina=5
					dpt.tipo_doc="P"
					dpt.correlativo=ut.proforma
					dpt.save()
			tienda=usu.tienda
			context={
			"tienda":tienda.nombre,
			"store":tienda.id,
			"accion":"imprimir"
			}
			return render(request, plantilla, context)

		return redirect("/")


class menu_proforma(TemplateView):
	template_name = "productos/proforma/index/"
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			usu=getPerfil(request)
			context={
				"tienda":usu.tienda
			}
			pl = self.template_name+obtenerPlantilla(request)
			return render(request,pl,context)
		return redirect("/")




class factura(TemplateView):
	template_name="impresion/documento.html"
	def get(self,request,id=None,*args,**kwargs):
		if OKpeople(request):
			his = PROFORMA.objects.get(id=id)
			name = his.lista.ubicado.tienda.nombre
			paginas = LISTA_PRODUCTO.objects.filter(lista=his.lista).count()/10
			bus=his.lista.ubicado.tienda
			name=bus.nombre
			addr=bus.direccion
			phone = bus.telefono
			nit= bus.nit
			comunicado="El siguiente documento es una proforma generada en la empresa <b>'"+name+"'</b>. La misma esta sujeta a cambios de marca o inventario."
			comunicado+=" Aplica restricciones, valido de <b>"+str(his.fehca_registro)+" a "+str(his.fecha_vencimiento)+"</b>, también puede comunicarse con su asesor en ventas: <b>'"+his.vendedor.nombre+" "+his.vendedor.apellido+"'</b> al numero de telefono: '"+his.vendedor.telefono+"'</br> <button onclick='back()'> << </button><script>function back(){window.history.back();}</script>"
			context={
				"nombre_empresa":name,
				"addr":addr,
				"nit_E":nit,
				"tipo":"PROFORMA",
				"telefono":"PBX:"+phone,
				"numero":id,
				"fecha":his.fehca_registro,
				"nit":" NUMERO DE CONTACTO:"+his.telefono,
				"nombre":his.atencion,
				"direccion":his.correo,
				"credito":"--",
				"solicitud":"asesorado por:",
				"usuario":his.lista.ubicado.usuario.usuario.username,
				"paginas":paginas,
				"lista":his.lista,
				"comunicado":comunicado,
				"total_documento":his.lista.total
			}
			return render(request,self.template_name,context)

		return redirect("/")
