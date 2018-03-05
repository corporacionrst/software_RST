from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from software_RST.settings.celery import app
from channels import Group
from channels import Channel

from django.db.models import Q

from ....cliente_proveedor.persona.models import PERSONA
from ....cliente_proveedor.proveedor.models import PROVEEDOR
from ....sistema.usuarios.models import Perfil,DOCUMENTO_POR_TIENDA,PUESTO,USUARIO_TIENDA
from ..inventario.models import INVENTARIO
from ....alertas.models import ALERTA
from .models import ORDEN_DE_COMPRA
from ..historial.models import LISTA_PRODUCTO,HISTORIAL
from ....factores import *

from datetime import date

import json

@app.task
def solicitud_orden(nnit,cr,usu,reply_channel):
	nit = PERSONA.objects.get(nit=nnit)
	proveedor = PROVEEDOR.objects.filter(info=nit)
	proveedor=proveedor[0]
	usuario = Perfil.objects.filter(usuario__id=usu)[0]
	ut = USUARIO_TIENDA.objects.filter(usuario=usuario).filter(tienda=usuario.tienda)
	if ut.exists():
		ut=ut[0]
		dpt = DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=0).filter(correlativo=ut.orden)
		if dpt.exists():
			dpt=dpt[0]
			lp = LISTA_PRODUCTO.objects.filter(lista=dpt)
			if lp.exists():
				oc = ORDEN_DE_COMPRA()
				oc.proveedor=proveedor
				oc.solicita=dpt.ubicado.usuario
				oc.lista=dpt
				oc.save()
				exito="V"
				principal="orden de compra"
				instruccion="autorizacion"
				ruta="/orden_de_compra/pendientes"
				solicita=dpt.ubicado.usuario.usuario.username
				p=PUESTO.objects.filter(Q(nombre__icontains="admin"))
				alerta = ALERTA()
				alerta.mensaje=principal
				alerta.sub_mensaje=instruccion
				alerta.requiere=dpt.ubicado.usuario
				alerta.ruta=ruta
				alerta.puesto=p[0]
				alerta.tienda=dpt.ubicado.tienda
				alerta.save()
				ut = USUARIO_TIENDA.objects.get(id=dpt.ubicado.id)
				ut.orden=int(ut.orden)+1
				ut.save()
				dpt.credito=cr
				dpt.save()
				if reply_channel is not None:
					Group("alertas").send({
						"text": json.dumps ({
							"exito": exito,
							"tipo":"alerta",
							"principal": principal,
							"instruccion":instruccion,
							"solicita":solicita,
							"puesto":oc.solicita.puesto.nombre,
							"ruta":ruta
						})
					})
				else:
					if reply_channel is not None:
						Group("alertas").send({
							"text": json.dumps ({
								"exito": "F",
								"tipo":"alerta",
								"principal": "La lista",
								"instruccion":" parece estar vacia",
								"solicita":"",
								"puesto":"",
								"ruta":""
							})
						})


@app.task
def descartar_orden(no_orden,com,perfil,reply_channel):
	pr = Perfil.objects.filter(usuario__id=perfil)[0]
	oc = ORDEN_DE_COMPRA.objects.get(id=no_orden)
	oc.autorizo=pr
	oc.autorizada=False
	oc.save()
	alerta = ALERTA()
	alerta.tipo=1
	alerta.mensaje="orden rechazada"
	alerta.sub_mensaje="motivo: "+com
	alerta.requiere=oc.solicita
	alerta.ruta="/orden_de_compra/autorizadas"
	alerta.puesto=oc.solicita.puesto
	alerta.save()

	if reply_channel is not None:
		Group("alertas").send({
			"text": json.dumps ({
				"exito": "F",
				"tipo":"notificacion",
				"principal": "orden rechazada",
				"instruccion":"motivo: "+com,
				"solicita":oc.solicita.usuario.id,
				"ruta":"/orden_de_compra/autorizadas"
			})
		})


@app.task
def oc_visto(r):
	usu = Perfil.objects.get(id=r)
	aoc = ALERTA.objects.filter(tienda=usu.tienda).filter(tipo=0).filter(Q(mensaje__icontains="orden"))
	for a in aoc:
		a.visto=True
		a.save()

@app.task
def al_oc_visto(r):
	usu = Perfil.objects.get(id=r)
	aoc = ALERTA.objects.filter(tienda=usu.tienda).filter(requiere=usu).filter(tipo=1).filter(Q(mensaje__icontains="orden"))
	for a in aoc:
		a.visto=True
		a.save()


@app.task
def authorize_oc(info,usuario,reply_channel):
	oc= ORDEN_DE_COMPRA.objects.get(id=info)
	pr = Perfil.objects.get(id=usuario)
	oc.autorizada=True
	oc.autorizo=pr
	his = HISTORIAL()
	his.cliente_proveedor=oc.proveedor.info
	his.ingresa=pr
	his.fehca_registro=date.today()
	his.lista=oc.lista
	his.save()
	oc.documento=his
	oc.save()
	user_solicita = oc.solicita.usuario
	alerta = ALERTA()
	alerta.tipo=1
	alerta.mensaje="orden autorizada"
	alerta.sub_mensaje="ver"
	alerta.requiere=oc.solicita
	alerta.ruta="/orden_de_compra/autorizadas"
	alerta.puesto=oc.solicita.puesto
	alerta.save()
	lp = LISTA_PRODUCTO.objects.filter(lista=oc.lista)
	for l in lp:
		prod = INVENTARIO.objects.filter(tienda=oc.lista.ubicado.tienda).filter(producto=l.producto)
		if prod.exists():
			pr = prod[0]
			pr.cantidad=pr.cantidad+l.cantidad
			pr.costo=max(l.unitario,pr.costo)
			if l.producto.marca.importacion==True:
				pr.distribuidor=distribuidor(pr.distribuidor,l.unitario)
				pr.mayorista=mayorista(pr.mayorista,l.unitario)
				pr.efectivo=efectivo(pr.efectivo,l.unitario)
				pr.tarjeta =tarjeta(pr.tarjeta,l.unitario)
			else:
				pr.distribuidor=l_efectivo(pr.distribuidor,l.unitario)
				pr.mayorista=l_efectivo(pr.mayorista,l.unitario)
				pr.efectivo=l_efectivo(pr.efectivo,l.unitario)
				pr.tarjeta =l_precio(pr.tarjeta,l.unitario)
			pr.save()
		else:
			prod = INVENTARIO()
			prod.tienda= oc.lista.ubicado.tienda
			prod.producto = l.producto
			prod.cantidad = int(l.cantidad)
			prod.costo  = l.unitario
			if l.producto.marca.importacion==True:
				prod.distribuidor=distribuidor(0,l.unitario)
				prod.mayorista=mayorista(0,l.unitario)
				prod.efectivo=efectivo(0,l.unitario)
				prod.tarjeta =tarjeta(0,l.unitario)
			else:
				prod.distribuidor=l_efectivo(0,l.unitario)
				prod.mayorista=l_efectivo(0,l.unitario)
				prod.efectivo=l_efectivo(0,l.unitario)
				prod.tarjeta =l_precio(0,l.unitario)
			prod.save()
	if reply_channel is not None:
		Group("alertas").send({
			"text": json.dumps ({
				"exito": "V",
				"tipo":"notificacion",
				"principal": "orden autorizada",
				"instruccion":"ver",
				"solicita":user_solicita.id,
				"ruta":"/orden_de_compra/autorizadas"
			})
		})
	


	

