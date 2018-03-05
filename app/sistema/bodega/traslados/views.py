# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from ....request_session import OKbodega,getPerfil
from ...tienda.models import EMPRESA
from ....productos.inventario.inventario.models import INVENTARIO
from ....productos.producto.models import PRODUCTO
from .models import TRASLADO, NO_TRASLADO,TRASLADO_AUTORIZADO

from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json

from datetime import date, timedelta

import datetime
from .tasks import limpiar_traslados_tienda

class listar(TemplateView):
	def get(self,request,*args,**kwargs):
		return redirect("/")
	

class recuperar(TemplateView):
	def get(self,request,*args,**kwargs):
		return redirect("/")


class traslados_vista_previa(TemplateView):
	template_view="productos/traslados/lista.html"
	def get(self,request,id=None,*args,**kwargs):
		ta = TRASLADO_AUTORIZADO.objects.get(id=id)
		producto=TRASLADO.objects.filter(no=ta.no).filter(numero=ta.indice)
		context={
		"hola":"adios",
		"producto":producto
		}
		return render(request,self.template_view,context)



class autorizar_traslados(TemplateView):
	template_view="productos/traslados/autorizar.html"
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			usu=getPerfil(request)
			ltt=limpiar_traslados_tienda.delay(usu.tienda.id)
			tr= TRASLADO_AUTORIZADO.objects.filter(no__de=usu.tienda).filter(autoriza__isnull=True)[0:10]
			context={
				"tienda":usu.tienda,
				"traslados":tr
			}
			return render(request,self.template_view,context)
		return redirect("/")
# Create your views here.
class quitar_lista_traslado(TemplateView):
	def post(self,request,*args,**kwargs):
		if OKbodega(request):
			de=EMPRESA.objects.get(id=int(request.POST['tienda']))
			a=getPerfil(request).tienda
			producto=PRODUCTO.objects.get(id=request.POST['producto'])
			nt=NO_TRASLADO.objects.filter(de=de).filter(a=a)
			if nt.exists():
				nt=nt[0]
				tr=TRASLADO.objects.filter(no=nt).filter(numero=nt.numero).filter(producto=producto)
				if tr.exists():
					tr=tr[0]
					tr.delete()
				traslado = TRASLADO.objects.filter(no=nt).filter(numero=nt.numero).values("producto__id","producto__codigo","producto__descripcion","producto__marca","cantidad","venta")[0:10]
				traslado=json.dumps(list(traslado),cls=DjangoJSONEncoder)
				return HttpResponse(traslado,content_type='application/json')
		return HttpResponse("{}",content_type='application/json')




class cargar_a_lista_traslado(TemplateView):
	def post(self,request,*args,**kwargs):
		if OKbodega(request):
			de=EMPRESA.objects.get(id=int(request.POST['tienda']))
			a=getPerfil(request).tienda
			producto=PRODUCTO.objects.get(id=request.POST['producto'])
			cantidad=int(request.POST['cantidad'])
			inv = INVENTARIO.objects.filter(tienda=de).filter(producto=producto)
			nt=NO_TRASLADO.objects.filter(de=de).filter(a=a)
			if not nt.exists():
				nt=NO_TRASLADO()
				nt.de=de
				nt.a=a
				nt.numero=1
				nt.total=0
				nt.save()
			else:
				nt=nt[0]
			tr=TRASLADO.objects.filter(no=nt).filter(numero=nt.numero).filter(producto=producto)
			if not tr.exists():
				if cantidad<=inv[0].cantidad:
					tr=TRASLADO()
					tr.no=nt
					tr.fecha=datetime.datetime.now()
					tr.numero=nt.numero
					tr.producto=producto
					tr.venta=inv[0].tarjeta
					tr.cantidad=cantidad
					tr.save()
					nt.total=nt.total+(cantidad*inv[0].tarjeta)
					nt.save()
			traslado = TRASLADO.objects.filter(no=nt).filter(numero=nt.numero).values("producto__id","producto__codigo","producto__descripcion","producto__marca","cantidad","venta")[0:10]
			traslado=json.dumps(list(traslado),cls=DjangoJSONEncoder)
			return HttpResponse(traslado,content_type='application/json')
		return HttpResponse("{}",content_type='application/json')







class tienda_trasladar(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			de=request.GET["tienda"]
			a=getPerfil(request).tienda
			pag=int(request.GET['pag'])*10
			numero= NO_TRASLADO.objects.filter(de=de).filter(a=a)
			if numero.exists():
				tr = TRASLADO.objects.filter(no=numero[0]).filter(numero=numero[0].numero)
				tr=tr.values("producto__id","producto__codigo","producto__descripcion","producto__marca","cantidad","venta")[pag:pag+10]
				tr=json.dumps(list(tr),cls=DjangoJSONEncoder)
				return HttpResponse(tr,content_type='application/json')
		return HttpResponse("{}",content_type='application/json')
		

class index_traslados(TemplateView):
	template_name="productos/traslados/generar.html"
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			usu = getPerfil(request)
			context={
			"tienda":usu.tienda
			}
			return render(request,self.template_name,context)
		else:
			return redirect("/")


class generar_traslado(TemplateView):
	template_name="productos/traslados/generar.html"
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			tienda=getPerfil(request).tienda
			empresa= EMPRESA.objects.exclude(id=tienda.id)
			context={
				"tienda":tienda,
				"empresa":empresa,
				"id_tienda":tienda.id
			}
			return render(request,self.template_name,context)

		else:
			return redirect("/")


class cargar_a_traslado(TemplateView):
	def post(self,request,*args,**kwargs):
		if OKbodega(request):
			de=EMPRESA.objects.get(id=int(request.POST["tienda"]))
			a=getPerfil(request).tienda
			pr=request.POST['producto']
			producto=PRODUCTO.objects.get(id=pr)
			cantidad =int(request.POST['cantidad'])
			numero= NO_TRASLADO.objects.filter(de=de).filter(a=a)
			pr_inv=INVENTARIO.objects.filter(tienda=de).filter(producto=producto)
			if numero.exists():
				if pr_inv.cantidad<cantidad:
					return HttpResponse("La cantidad solicitada no puede ser despachada")
				tr = TRASLADO.objects.filter(no=numero[0]).filter(numero=numero.numero).filter(producto=producto)
				if tr.exists():
					return HttpResponse("este producto ya fue cargado, favor revisar",content_type="text")
				else:
					tr = TRASLADO()
					tr.no=numero[0]
					tr.fecha=datetime.datetime.now()
					tr.numero=numero[0].numero
					tr.producto=producto
					tr.cantidad=cantidad
					tr.venta=pr_inv.tarjeta
					tr.save()
					total=numero[0]
					total=total.total+(cantidad*pr_inv[0].tarjeta)
					total.save()
			else:
				if pr_inv.cantidad<cantidad:
					return HttpResponse("La cantidad solicitada no puede ser despachada")
				numero=NO_TRASLADO()
				numero.de=de
				numero.a=a
				numero.save()
				tr = TRASLADO()
				tr.no=numero
				tr.fecha=datetime.datetime.now()
				tr.numero=1
				tr.producto=producto
				tr.cantidad=cantidad
				tr.venta=pr_inv.tarjeta
				tr.save()
				numero.total=cantidad*pr_inv[0].tarjeta
				numero.save()
			return HttpResponse("v",content_type='text')	
		return HttpResponse("no tienes permiso para realizar esta accion",content_type='text')
