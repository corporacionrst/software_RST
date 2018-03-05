from __future__ import unicode_literals


from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.http import HttpResponse
from ....request_session import *
import json
from decimal import Decimal
from ....sistema.tienda.models import EMPRESA
from ....sistema.usuarios.models import DOCUMENTO_POR_TIENDA,USUARIO_TIENDA
from ...producto.models import PRODUCTO,PRODUCTO_IMAGEN,PRODUCTO_SET
from ...detalle.models import FICHA_TECNICA

from ..historial.models import LISTA_PRODUCTO
from .models import INVENTARIO

from django.db.models import Q


class consulta_pagina_tienda(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			producto=request.GET['codigo']
			tienda = request.GET['tienda']
			empresa= EMPRESA.objects.get(id=tienda)
			i=int(request.GET['pagina'])*10
			if producto!="":
				qs=INVENTARIO.objects.filter(tienda=empresa).filter(Q(producto__codigo__nombre__icontains=producto)|Q(producto__descripcion__detalle__icontains=producto)).values('producto__id','producto__codigo','producto__descripcion','producto__marca','cantidad','tarjeta').order_by('producto__codigo')[i:i+10]
				qs=json.dumps(list(qs),cls=DjangoJSONEncoder)
				return HttpResponse(qs,content_type='application/json')
		return HttpResponse("{}",content_type='application/json')




# import pyqrcode
# url = pyqrcode.create('http://www.corporacionrst.com')
# url.svg('uca-url.svg', scale=8)
# print(url.terminal(quiet_zone=1))


class info_detallada(TemplateView):
	template_name="productos/inventario/detalle.html"
	def get(self,request,id=None,*args,**kwargs):
		if OKpeople(request):
			producto=PRODUCTO.objects.get(id=id)
			inv = INVENTARIO.objects.filter(producto=producto)
			img = PRODUCTO_IMAGEN.objects.filter(producto=producto)
			detalle=FICHA_TECNICA.objects.filter(listado=producto.detalles)
			id_set=PRODUCTO_SET.objects.filter(id_set=producto.id_set)
			context={
			"producto":id,
			"titulo":producto.codigo,
			"marca":producto.marca,
			"inventario":inv,
			"imagen":img,
			"index":img,
			"detalle":detalle,
			"set":id_set,

			}
			return render(request,self.template_name,context)

		else:
			return redirect("/")


class inventario_local(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			producto=request.GET['codigo']
			i=int(request.GET['pagina'])*10
			tienda = getPerfil(request).tienda
			if producto!="":
				qs = INVENTARIO.objects.filter(Q(producto__codigo__nombre__icontains=producto)|Q(producto__descripcion__detalle__icontains=producto)).filter(tienda=tienda).values('producto__id','producto__codigo','producto__descripcion','producto__marca','cantidad','mayorista','efectivo','tarjeta').order_by('producto__codigo')[i:i+10]
				qs=json.dumps(list(qs),cls=DjangoJSONEncoder)
				return HttpResponse(qs,content_type='application/json')
		return HttpResponse("{}",content_type='application/json')


		


class total(TemplateView):
	def get(self,request,*args,**kwargs):
		doc=request.GET["doc"]
		try:
			total =DOCUMENTO_POR_TIENDA.objects.get(id=doc).total
			return HttpResponse(total,content_type="text")
		except:
			return HttpResponse("0",content_type="text")


class inventario(TemplateView):
	template_name="productos/inventario/inv/"
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			tienda=getPerfil(request).tienda
			plantilla=self.template_name+obtenerPlantilla(request)
			context={"tienda":tienda}
			return render(request, plantilla, context)
		return redirect("/")
		
class local(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			producto=request.GET['codigo']
			i=int(request.GET['pagina'])*10
			if producto!="":
				qs = PRODUCTO.objects.filter(Q(codigo__nombre__icontains=producto)|Q(descripcion__detalle__icontains=producto)).values('id','codigo','descripcion','marca').order_by('codigo')[i:i+10]
				qs=json.dumps(list(qs),cls=DjangoJSONEncoder)
				return HttpResponse(qs,content_type='application/json')
		return HttpResponse("{}",content_type='application/json')


class cargar_a_lista(TemplateView):
	def post(self,request,*args,**kwargs):
		if OKpeople(request):
			documento=request.POST['document']
			producto =request.POST['producto']
			cantidad =request.POST['cantidad']
			precio   =request.POST['precio']
			dpt =DOCUMENTO_POR_TIENDA.objects.get(id=documento)
			prod = PRODUCTO.objects.get(id=producto)
			lp=LISTA_PRODUCTO.objects.filter(lista=dpt).filter(producto=prod)
			if lp.exists():
				message="este elemento ya fue agregado previamente"
			else:
				lp=LISTA_PRODUCTO()
				lp.lista=dpt
				lp.producto = prod
				lp.cantidad = int(cantidad)
				lp.unitario = Decimal(precio)
				lp.save()
				dpt.total=dpt.total+(Decimal(cantidad)*Decimal(precio))
				dpt.save()
				message="agregado correctamente"

			return HttpResponse(message,content_type='text')

		return HttpResponse("{}",content_type='text')

class listar(TemplateView):
	def get(self,request,*args,**kwargs):
		pag=request.GET["pag"]
		doc=request.GET["doc"]
		try:
			us =DOCUMENTO_POR_TIENDA.objects.get(id=doc)
			i=int(pag)*5
			Lista=LISTA_PRODUCTO.objects.filter(lista=us).values("producto__codigo","producto__descripcion","producto__marca","cantidad","unitario","producto__id").order_by("producto__codigo")[i:i+5]
			Lista=json.dumps(list(Lista),cls=DjangoJSONEncoder)
			return HttpResponse(Lista,content_type="application/json")
			
		except :
			return HttpResponse("{}",content_type="application/json")
			


class quitar(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			documento=request.GET['document']
			producto =request.GET['producto']
			dpt =DOCUMENTO_POR_TIENDA.objects.get(id=documento)
			prod = PRODUCTO.objects.get(id=producto)
			lp=LISTA_PRODUCTO.objects.filter(lista=dpt).filter(producto=prod)
			if  lp.exists():
				dpt.total=dpt.total-(Decimal(lp[0].cantidad)*Decimal(lp[0].unitario))
				dpt.save()
				lp[0].delete()
				message="eliminado"
				return HttpResponse(message,content_type='text')
		return HttpResponse("no se encontro elemento para borrar",content_type='text')



