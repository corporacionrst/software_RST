# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from ....request_session import OKpeople,getPerfil,obtenerPlantilla

from django.views.generic import TemplateView
from ....productos.inventario.forms import *
from ...usuarios.models import USUARIO_TIENDA,DOCUMENTO_POR_TIENDA


from ....productos.inventario.historial.models import *
from ....productos.inventario.inventario.models import INVENTARIO
from ....productos.producto.models import PRODUCTO
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder

from ....cliente_proveedor.persona.models import PERSONA

import json
from decimal import Decimal
import datetime

from django.http import HttpResponse

class consulta_inv(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			producto=request.GET['codigo']
			usu = getPerfil(request)
			i=int(request.GET['pagina'])*10
			if producto!="":
				qs =INVENTARIO.objects.filter(tienda=usu.tienda).filter(Q(producto__codigo__nombre__icontains=producto)|Q(producto__descripcion__detalle__icontains=producto)).values('producto__id','producto__codigo','producto__descripcion','producto__marca','cantidad','efectivo','tarjeta').order_by('producto__id')[i:i+10]
				qs=json.dumps(list(qs),cls=DjangoJSONEncoder)
				return HttpResponse(qs,content_type='application/json')
		return HttpResponse("{}",content_type='application/json')



class quitar_prod_factura(TemplateView):
	def post(self,request,*args,**kwargs):
		if OKpeople(request):
			usu = getPerfil(request)
			indice = int(request.POST["indice"])
			if indice>0 and indice<5:
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
					dpt = DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=indice).filter(correlativo=correlativo).filter(tipo_doc="V")
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
			indice = int(request.GET['indice'])
			if indice>0 and indice<5:
				usu = getPerfil(request)
				ut = USUARIO_TIENDA.objects.filter(usuario=usu).filter(tienda=usu.tienda)
				if ut.exists():
					ut=ut[0]
					correlativo=0
					if indice==1:
						correlativo=ut.fac_1
					elif indice==2:
						correlativo=ut.fac_2
					elif indice==3:
						correlativo=ut.fac_3
					else:
						correlativo=ut.fac_4
					dpt=DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=indice).filter(correlativo=correlativo).filter(tipo_doc="V")
					if dpt.exists():
						dpt=dpt[0]
						total=dpt.total
						return HttpResponse(total,content_type="text")

		return HttpResponse("0",content_type="text")




class cargar_a_lista_factura(TemplateView):
	def post(self,request,*args,**kwargs):
		message="{}"
		if OKpeople(request):
			pag = int(request.POST['indice'])
			cantidad=request.POST['cantidad']
			if cantidad!="":
				if pag>0 and pag<5:
					producto =request.POST['producto']
					prod = PRODUCTO.objects.get(id=producto)
					cantidad =int(cantidad)
					precio   =request.POST['precio']
					usu = getPerfil(request)
					ut = USUARIO_TIENDA.objects.filter(usuario=usu).filter(tienda=usu.tienda)
					if ut.exists():
						ut=ut[0]
						correlativo=0
						if pag==1:
							correlativo=ut.fac_1
						elif pag==2:
							correlativo=ut.fac_2
						elif pag==3:
							correlativo=ut.fac_3
						else:
							correlativo=ut.fac_4
						dpt=DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=pag).filter(correlativo=correlativo).filter(tipo_doc="V")
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
									dpt.pagina=pag
									dpt.correlativo=ut.orden
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
			indice=int(request.GET['indice'])
			if indice<5 and indice>0:
				ut = USUARIO_TIENDA.objects.filter(usuario=perfil).filter(tienda=perfil.tienda)
				if ut.exists():
					ut=ut[0]
					correlativo=0
					if indice==1:
						correlativo=ut.fac_1
					elif indice==2:
						correlativo=ut.fac_2
					elif indice==3:
						correlativo=ut.fac_3
					else:
						correlativo=ut.fac_4
					dpt =DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=indice).filter(correlativo=correlativo).filter(tipo_doc="V")
					if dpt.exists():
						dpt=dpt[0]
						i=int(request.GET["pag"])*5
						Lista=LISTA_PRODUCTO.objects.filter(lista=dpt).values("producto__codigo","producto__descripcion","producto__marca","cantidad","unitario","producto__id").order_by("producto__codigo")[i:i+5]
						Lista=json.dumps(list(Lista),cls=DjangoJSONEncoder)
						return HttpResponse(Lista,content_type="application/json")
					
		return HttpResponse("{}",content_type="application/json")
			






class registrar_venta(TemplateView):
	def post(self,request,*args,**kwargs):
		if OKbodega(request):
			nnit=request.POST["nit"].upper()
			info=request.POST["info"]
			cr=request.POST["credito"]
			credito=False
			if cr=="true":
				credito=True
			mensaje=""
			nit=PERSONA.objects.get(nit=nnit)
			us =DOCUMENTO_POR_TIENDA.objects.get(id=info)
			lp = LISTA_PRODUCTO.objects.filter(lista=us)
			if lp.exists():
				cargar=historial_ventas.delay(doc,nnit,credito,info,fecha)
				ut = USUARIO_TIENDA.objects.get(id=us.ubicado.id)
				ut.actual=int(ut.actual)+1
				ut.save()
				mensaje="V"
			else:
				mensaje="la lista parece estar vacia"
			
		else:
			return HttpResponse("no tienes permisos para registrar una compra",content_type='text')







class factura_no(TemplateView):
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



class menu_facturacion(TemplateView):
	template_name="facturacion/menu/"
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			usu = getPerfil(request)
			pl= obtenerPlantilla(request)
			context={
			"tienda":usu.tienda,
			"mensaje":""
			}
			return render(request,self.template_name+pl,context)
		return redirect("/")
	def post(self,request,*args,**kwargs):
		if OKpeople(request):
			nit=str(request.POST["nit"]).upper()
			credito=request.POST["credito"]
			pag=request.POST["pag"]
			usuario = getPerfil(request)
			pl= obtenerPlantilla(request)
			ut =USUARIO_TIENDA.objects.filter(usuario=usuario).filter(tienda=usuario.tienda)
			if ut.exists() and pag!="":
				pag=int(pag)
				if pag>0 and pag<5:
					ut=ut[0]
					correlativo=0
					if pag==1:
						correlativo=ut.fac_1
						ut.fac_1=ut.fac_1+1
					elif pag==2:
						correlativo=ut.fac_2
						ut.fac_2=ut.fac_2+1
					elif pag==3:
						correlativo=ut.fac_3
						ut.fac_3=ut.fac_3+1
					else:
						correlativo=ut.fac_4
						ut.fac_4=ut.fac_4+1
					dpt = DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=pag).filter(correlativo=correlativo).filter(tipo_doc="V")
					if dpt.exists():
						dpt=dpt[0]
						lp = LISTA_PRODUCTO.objects.filter(lista=dpt)
						if not lp.exists():
							mensaje="la lista parece estar vacia"
						else:
							mensaje="documento en caja"
							if "true" in credito:
								dpt.credito=True
								dpt.save()
							cp = PERSONA.objects.get(nit=nit)
							h = HISTORIAL()
							h.cliente_proveedor=cp
							h.fehca_registro=datetime.datetime.now()
							h.ingresa=usuario
							h.lista=dpt
							h.save()
							ut.save()
						context={
							"tienda":usuario.tienda,
							"mensaje":mensaje
						}
						return HttpResponse("Documento en caja",content_type='text')
			return HttpResponse("no existe el documento",content_type='text')
		return HttpResponse("no tienes permisos para registrar una compra",content_type='text')
