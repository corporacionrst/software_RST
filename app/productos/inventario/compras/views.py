# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q

from ..forms import *
import json

from django.core.serializers.json import DjangoJSONEncoder
from ....request_session import OKbodega,getPerfil,OKconta,OKadmin
from ....sistema.usuarios.models import Perfil,DOCUMENTO_POR_TIENDA,USUARIO_TIENDA
from ....cliente_proveedor.proveedor.tasks import crear_proveedor
from ....cliente_proveedor.persona.models import PERSONA
from ..historial.models import HISTORIAL,LISTA_PRODUCTO

from .tasks import historial_compras

# Create your views here.

class detallar_compra(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKconta(request):
			doc= request.GET['documento']
			i = int(request.GET['pag'])*10
			l =DOCUMENTO_POR_TIENDA.objects.get(id=doc)
			lp=LISTA_PRODUCTO.objects.filter(lista=l).values("producto__codigo","producto__descripcion","producto__marca","cantidad","unitario")
			lp=json.dumps(list(lp),cls=DjangoJSONEncoder)
			return HttpResponse(lp,content_type='application/json')
		else:
			return HttpResponse("{}",content_type='application/json')



class documento(TemplateView):
	def get(self,request,*args,**kwargs):
		ok = OKconta(request)
		if OKbodega(request) or ok:
			bus = request.GET["busca"]
			bus=bus.upper()
			i= request.GET["index"]
			pag = int(request.GET["pag"])*10
			if i=="1":
				cp = PERSONA.objects.get(nit=bus)
				his = HISTORIAL.objects.filter(cliente_proveedor=cp).filter(Q(lista__tipo_doc__icontains="C"))[pag:pag+10]
			else:
				his = HISTORIAL.objects.filter(Q(documento__icontains=bus)).filter(Q(lista__tipo_doc__icontains="C"))[pag:pag+10]

			his=his.values("documento","cliente_proveedor__nit","lista__id","ingresa__usuario__username","lista__total")
			his=json.dumps(list(his),cls=DjangoJSONEncoder)
			return HttpResponse(his,content_type='application/json')

		else:
			return HttpResponse("{}",content_type='application/json')





class ver_compras(TemplateView):
	template_name="productos/inventario/compras/compras.html"
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			context={
			"tienda":getPerfil(request).tienda.nombre,
			}
			return render(request, self.template_name, context)
		return redirect("/")



	

class inv_local(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			pr = int(request.GET['producto'])
			qs = PRODUCTO.objects.get(id=pr).id_set
			if qs==None:
				qs=Perfil.objects.get(usuario=request.user).documento4
			return HttpResponse(qs,content_type='text')	
		return HttpResponse("{}",content_type='text')


class cargar_factura(TemplateView):
	template_name="productos/inventario/compras/cargar.html"
	formU = FormPersona
	url = "/proveedores/nit"
	initial={'key':'value'}
	formulario=Form_registrar
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			usu= getPerfil(request)
			ubicacion = USUARIO_TIENDA.objects.filter(usuario=usu).filter(tienda=usu.tienda)
			lis=0
			if not ubicacion.exists():
				ubicacion=USUARIO_TIENDA()
				ubicacion.usuario=usu
				ubicacion.tienda=usu.tienda
				ubicacion.save()
				lpt=DOCUMENTO_POR_TIENDA()
				lpt.ubicado=ubicacion
				lpt.tipo_doc="C"
				lpt.save()
				lis=lpt.id
			else:
				lpt = DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ubicacion[0]).filter(tipo_doc="C").filter(correlativo=ubicacion[0].orden)
				if not lpt.exists():
					lpt=DOCUMENTO_POR_TIENDA()
					lpt.ubicado=ubicacion[0]
					lpt.tipo_doc="C"
					lpt.correlativo=ubicacion[0].orden
					lpt.save()
					lis=lpt.id
				else:
					lis=lpt[0].id
			tienda=usu.tienda
			form=self.formU(initial=self.initial)
			fm = self.formulario(initial=self.initial)
			tienda=getPerfil(request).tienda
			context={
			"tienda":tienda.nombre,
			"store":tienda.id,
			"form":form,
			"formulario":fm,
			"url":self.url,
			"accion":"cargar compra",
			"lista":lis
			}
			return render(request, self.template_name, context)
		return redirect("/")


class registrar_compra(TemplateView):
	def post(self,request,*args,**kwargs):
		if OKbodega(request):
			doc=request.POST["documento"].upper()
			nnit=request.POST["nit"].upper()
			fecha=request.POST["fecha"]
			cr=request.POST["credito"]
			credito=False
			if cr=="true":
				credito=True
			mensaje=""
			nit=PERSONA.objects.get(nit=nnit)
			his = HISTORIAL.objects.filter(documento=doc).filter(cliente_proveedor=nit).filter(lista__tipo_doc="C")
			if his.exists():
				mensaje="Un archivo similar existe ya registrado,favor revisar"
			else:
				usu=getPerfil(request)
				dpt =DOCUMENTO_POR_TIENDA.objects.filter(ubicado__usuario=usu).filter(ubicado__tienda=usu.tienda).filter(tipo_doc="C")
				if dpt.exists():
					dpt=dpt[0]
					lp = LISTA_PRODUCTO.objects.filter(lista=dpt)
					if lp.exists():
						cargar=historial_compras.delay(doc,nnit,credito,dpt.id,fecha)
						ut = USUARIO_TIENDA.objects.get(id=dpt.ubicado.id)
						ut.orden=int(ut.orden)+1
						ut.save()
						mensaje="V"
					else:
						mensaje="la lista parece estar vacia"
				else:
					mensaje="la lista parece estar vacia"

					
			return HttpResponse(mensaje,content_type='text')
		else:
			return HttpResponse("no tienes permisos para registrar una compra",content_type='text')








