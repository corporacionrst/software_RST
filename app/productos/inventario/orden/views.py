# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect

from django.views.generic import TemplateView

from django.core.serializers.json import DjangoJSONEncoder
import json

from .forms import Login_O_Form
from ..forms import *
from django.http import HttpResponse
# from ..compras.models import COMPRAS
import json

from ..historial.models import LISTA_PRODUCTO
from django.core.serializers.json import DjangoJSONEncoder
from ....sistema.usuarios.models import Perfil,DOCUMENTO_POR_TIENDA,USUARIO_TIENDA
from ....cliente_proveedor.proveedor.tasks import crear_proveedor
from ....cliente_proveedor.persona.models import PERSONA
from....request_session import *
from .models import ORDEN_DE_COMPRA
from ...producto.models import PRODUCTO


from decimal import Decimal


from ....sistema.cobros.contrasena.models import CONTRASENA

from .tasks import solicitud_orden,descartar_orden,oc_visto,authorize_oc,al_oc_visto


class cargar_a_lista_compra(TemplateView):
	def post(self,request,*args,**kwargs):
		message="{}"
		if OKpeople(request):
			producto =request.POST['producto']
			cantidad =request.POST['cantidad']
			precio   =request.POST['precio']
			usu = getPerfil(request)
			ut = USUARIO_TIENDA.objects.filter(usuario=usu).filter(tienda=usu.tienda)
			prod = PRODUCTO.objects.get(id=producto)
			if ut.exists():
				ut=ut[0]
				dpt=DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=0).filter(correlativo=ut.actual).filter(tipo_doc="C")
				if dpt.exists():
					dpt=dpt[0]
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
					dpt=DOCUMENTO_POR_TIENDA()
					dpt.ubicado=ut
					dpt.pagina=0
					dpt.correlativo=ut.actual
					dpt.tipo_doc="C"
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
				ut=USUARIO_TIENDA()
				ut.usuario=usu
				ut.tienda=ut.tienda
				ut.save()
				dpt=DOCUMENTO_POR_TIENDA()
				dpt.ubicado=ut
				dpt.pagina=0
				dpt.tipo_doc="C"
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

		return HttpResponse(message,content_type='text')



class quitar_prod_compra(TemplateView):
	def post(self,request,*args,**kwargs):
		if OKpeople(request):
			usu = getPerfil(request)
			ut = USUARIO_TIENDA.objects.filter(usuario=usu).filter(tienda=usu.tienda)
			if ut.exists():
				ut=ut[0]
				dpt = DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=0).filter(correlativo=ut.actual).filter(tipo_doc="C")
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




class total_compra(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			usu = getPerfil(request)
			ut = USUARIO_TIENDA.objects.filter(usuario=usu).filter(tienda=usu.tienda)
			if ut.exists():
				ut=ut[0]
				dpt=DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=0).filter(correlativo=ut.actual).filter(tipo_doc="C")
				if dpt.exists():
					dpt=dpt[0]
					total=dpt.total
					return HttpResponse(total,content_type="text")

		return HttpResponse("0",content_type="text")


class listar_compra(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			perfil = getPerfil(request)
			ut = USUARIO_TIENDA.objects.filter(usuario=perfil).filter(tienda=perfil.tienda)
			if ut.exists():
				ut=ut[0]
				us =DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=0).filter(correlativo=ut.actual).filter(tipo_doc="C")
				if us.exists():
					try:
						us=us[0]
						i=int(request.GET["pag"])*5
						Lista=LISTA_PRODUCTO.objects.filter(lista=us).values("producto__codigo","producto__descripcion","producto__marca","cantidad","unitario","producto__id").order_by("producto__codigo")[i:i+5]
						Lista=json.dumps(list(Lista),cls=DjangoJSONEncoder)
						return HttpResponse(Lista,content_type="application/json")
					except:
						return HttpResponse("{}",content_type="application/json")
		return HttpResponse("{}",content_type="application/json")
			



class quitar_prod_oc(TemplateView):
	def post(self,request,*args,**kwargs):
		if OKpeople(request):
			usu = getPerfil(request)
			ut = USUARIO_TIENDA.objects.filter(usuario=usu).filter(tienda=usu.tienda)
			if ut.exists():
				ut=ut[0]
				dpt = DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=0).filter(correlativo=ut.orden).filter(tipo_doc="O")
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





class total_orden(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			usu = getPerfil(request)
			ut = USUARIO_TIENDA.objects.filter(usuario=usu).filter(tienda=usu.tienda)
			if ut.exists():
				ut=ut[0]
				dpt=DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=0).filter(correlativo=ut.orden).filter(tipo_doc="O")
				if dpt.exists():
					dpt=dpt[0]
					total=dpt.total
					return HttpResponse(total,content_type="text")

		return HttpResponse("0",content_type="text")




class cargar_a_lista_orden(TemplateView):
	def post(self,request,*args,**kwargs):
		message="{}"
		if OKpeople(request):
			producto =request.POST['producto']
			cantidad =request.POST['cantidad']
			precio   =request.POST['precio']
			usu = getPerfil(request)
			ut = USUARIO_TIENDA.objects.filter(usuario=usu).filter(tienda=usu.tienda)
			prod = PRODUCTO.objects.get(id=producto)
			if ut.exists():
				ut=ut[0]
				dpt=DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=0).filter(correlativo=ut.orden).filter(tipo_doc="O")
				if dpt.exists():
					dpt=dpt[0]
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
					dpt=DOCUMENTO_POR_TIENDA()
					dpt.ubicado=ut
					dpt.pagina=0
					dpt.correlativo=ut.orden
					dpt.tipo_doc="O"
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
				ut=USUARIO_TIENDA()
				ut.usuario=usu
				ut.tienda=ut.tienda
				ut.save()
				dpt=DOCUMENTO_POR_TIENDA()
				dpt.ubicado=ut
				dpt.pagina=0
				dpt.tipo_doc="O"
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

		return HttpResponse(message,content_type='text')



class listar_datos_orden(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			perfil = getPerfil(request)
			ut = USUARIO_TIENDA.objects.filter(usuario=perfil).filter(tienda=perfil.tienda)
			if ut.exists():
				ut=ut[0]
				us =DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=0).filter(correlativo=ut.orden).filter(tipo_doc="O")
				if us.exists():
					try:
						us=us[0]
						i=int(request.GET["pag"])*5
						Lista=LISTA_PRODUCTO.objects.filter(lista=us).values("producto__codigo","producto__descripcion","producto__marca","cantidad","unitario","producto__id").order_by("producto__codigo")[i:i+5]
						Lista=json.dumps(list(Lista),cls=DjangoJSONEncoder)
						return HttpResponse(Lista,content_type="application/json")
					except:
						return HttpResponse("{}",content_type="application/json")
		return HttpResponse("{}",content_type="application/json")
			





class menuOrden(TemplateView):
	template_name="productos/orden/menu/menu_"
	def get(self,request,*args,**kwargs):
		plantilla= self.template_name
		if not OKpeople(request):
			return redirect("/")
		else:
			profile = getPerfil(request)
			odc= ORDEN_DE_COMPRA.objects.filter(solicita=profile).filter(lista__ubicado__tienda=profile.tienda)
			contar_pendiente=odc.filter(autorizo__isnull=True).count()
			contar_autorizada=odc.filter(autorizada=True).filter(impreso=False).count()
			plantilla=plantilla+obtenerPlantilla(request)
			usu= getPerfil(request)
			tienda = usu.tienda
			context={
			"tienda":tienda.nombre,
			"store":tienda.id,
			"pendiente":contar_pendiente,
			"autorizada":contar_autorizada
			}
			return render(request, plantilla, context)



class cargar_orden_de_compra(TemplateView):
	template_name="productos/orden/"
	formU = FormPersona
	url = "/proveedores/nit"
	initial={'key':'value'}
	formulario=Form_registrar
	def get(self,request,*args,**kwargs):
		plantilla=self.template_name
		if not OKpeople(request):
			return redirect("/")
		else:
			plantilla=plantilla+obtenerPlantilla(request)
			usu= getPerfil(request)
			ut = USUARIO_TIENDA.objects.filter(usuario=usu).filter(tienda=usu.tienda)
			if ut.exists():
				ut=ut[0]
				dpt = DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=0).filter(tipo_doc="O").filter(correlativo=ut.orden)
				if not dpt.exists():
					dpt=DOCUMENTO_POR_TIENDA()
					dpt.ubicado=ut
					dpt.correlativo=ut.orden
					dpt.tipo_doc="O"
					dpt.save()
			else:
				ut=USUARIO_TIENDA()
				ut.usuario=usu
				ut.tienda=usu.tienda
				ut.save()
				dpt=DOCUMENTO_POR_TIENDA()
				dpt.ubicado=ut
				dpt.tipo_doc="O"
				dpt.save()
			form=self.formU(initial=self.initial)
			fm = self.formulario(initial=self.initial)
			context={
			"tienda":usu.tienda.nombre,
			"store":usu.tienda.id,
			"form":form,
			"formulario":fm,
			"url":self.url,
			"accion":"solicitar orden de compra",
			}
			return render(request, plantilla, context)
		return redirect("/")



class ordenes_pendientes(TemplateView):
	template_name="productos/orden/lista_pendientes.html"
	def get(self,request,*args,**kwargs):
		if OKadmin(request):
			usu= getPerfil(request)
			task_id=oc_visto.delay(usu.id)
			tienda=usu.tienda
			context={
				"tienda":tienda.nombre
			}	
			return render(request, self.template_name, context)
		return redirect("/")


class cargar_listado_credito(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKadmin(request):
			pag = int(request.GET['pag'])*10
			us = getPerfil(request)
			oc = ORDEN_DE_COMPRA.objects.filter(lista__ubicado__tienda=us.tienda).filter(autorizo__isnull=True).filter(lista__credito=True)
			if oc.exists():
				oc=oc.values("proveedor__info__nombre","solicita__usuario__username","fecha_registro","lista__total","id")
				oc=json.dumps(list(oc),cls=DjangoJSONEncoder)
				return HttpResponse(oc,content_type='application/json')	
			else:
				return HttpResponse("{}",content_type='application/json')

		else:
			return HttpResponse("{}",content_type='application/json')

class cargar_listado_contado(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKadmin(request):
			pag = int(request.GET['pag'])*10
			us = getPerfil(request)
			oc = ORDEN_DE_COMPRA.objects.filter(lista__ubicado__tienda=us.tienda).filter(autorizo__isnull=True).filter(lista__credito=False)
			if oc.exists():
				oc=oc.values("proveedor__info__nombre","solicita__usuario__username","fecha_registro","lista__total","id")
				oc=json.dumps(list(oc),cls=DjangoJSONEncoder)
				return HttpResponse(oc,content_type='application/json')	
			else:
				return HttpResponse("{}",content_type='application/json')

		else:
			return HttpResponse("{}",content_type='application/json')




class ordenes_autorizadas(TemplateView):
	template_name="productos/orden/autorizada/"
	orden=Login_O_Form
	def get(self,request,*args,**kwargs):
		if not OKpeople(request):
			context={
			"form":self.orden
			}
			return render(request, self.template_name+"invitado.html", context)
		else:
			usu = getPerfil(request)
			plantilla= self.template_name	
			profile = getPerfil(request)
			task_id=al_oc_visto.delay(usu.id)
			odc= ORDEN_DE_COMPRA.objects.filter(solicita=profile).filter(lista__ubicado__tienda=profile.tienda).filter(autorizada=True).filter(impreso=False)
			contar_pendiente=odc.filter(autorizo__isnull=True).count()
			contar_autorizada=odc.filter(autorizada=True).count()
			plantilla=plantilla+obtenerPlantilla(request)
			usu= getPerfil(request)
			tienda = usu.tienda
			context={
			"tienda":tienda.nombre,
			"store":tienda.id,
			"pendiente":contar_pendiente,
			"orden":odc,
			"autorizada":contar_autorizada
			}
			return render(request, plantilla, context)
	def post(self,request,*args,**kwargs):
		form = self.orden(request.POST)
		if form.is_valid():
			no =form.cleaned_data["orden_de_compra"]
			return imprimir_orden(request,no)	
		return redirect("/orden_de_compra/autorizadas/")
	



def check_oc(nit,credito,usu,reply_channel):
	task_id= solicitud_orden.delay(nit,credito,usu,reply_channel)

def quit_orden(no_orden,com,usuario,reply_channel):
	task_id=descartar_orden.delay(no_orden,com,usuario,reply_channel)

def ok_oc(info,usuario,reply_channel):
	task_id=authorize_oc.delay(info,usuario,reply_channel)




def imprimir_orden(request, id=None):
	odc = ORDEN_DE_COMPRA.objects.filter(id=id).filter(autorizada=True)
	if not odc.exists():
		return redirect("/orden_de_compra/autorizadas/")
	else:
		odc=odc[0]
		paginas = LISTA_PRODUCTO.objects.filter(lista=odc.lista).count()/10
		bus=odc.lista.ubicado.tienda
		name=bus.nombre
		addr=bus.direccion
		phone = bus.telefono
		nit= bus.nit
		comunicado=" El siguiente documento es una orden de compra generada y autorizada por la empresa '"+name+"' para el control del ingreso de productos. Este documento no representa pago de contraseña, ni que una factura fue recibida. Para obtener su contraseña, presentar este documento con la copia de la factura original adjunta. para mas informacion, ingrese <a href='https://www.corporacionrst.com/orden_de_compra/autorizadas/'>aqui (usuario=nit,clave="+id+")</a>"
		if odc.lista.credito:
			credito="CREDITO"
		else:
			credito="CONTADO"
		context={
			"nombre_empresa":name,
			"addr":addr,
			"nit_E":nit,
			"tipo":"ORDEN DE COMPRA",
			"telefono":"PBX:"+phone,
			"numero":odc.id,
			"fecha":odc.fecha_registro,
			"nit":odc.proveedor.info.nit,
			"nombre":odc.proveedor.info.nombre,
			"direccion":odc.proveedor.info.direccion,
			"credito":credito,
			"solicitud":"solicita",
			"usuario":odc.solicita.usuario.username,
			"paginas":paginas,
			"lista":odc.lista,
			"comunicado":comunicado,
			"total_documento":odc.lista.total
		}
		return render(request,"impresion/documento.html",context)


class quitar(TemplateView):
	def post(self,request,*args,**kwargs):
		acreditar = request.POST["a_borrar"]
		odc = ORDEN_DE_COMPRA.objects.get(id=acreditar)
		odc.impreso=True
		odc.save()
		return HttpResponse("{}",content_type='application/json')


