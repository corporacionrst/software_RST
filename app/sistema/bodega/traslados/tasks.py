from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from software_RST.settings.celery import app
from channels import Group
from channels import Channel

from django.db.models import Q

from .models import NO_TRASLADO,TRASLADO,TRASLADO_AUTORIZADO
from ...usuarios.models import Perfil,PUESTO
from ...tienda.models import EMPRESA
from ....alertas.models import ALERTA
from ....productos.inventario.inventario.models import INVENTARIO


import json


@app.task
def autoriza_traslado(indice,comentario,autoriza,autorizada,reply_channel):
	TA=TRASLADO_AUTORIZADO.objects.get(id=indice)
	autorizador=Perfil.objects.get(id=autoriza)
	TA.autoriza=autorizador
	TA.recibe=comentario
	if autorizada=="V":
		TA.autorizada=True
		TA.save()
		if reply_channel is not None:
			Group("traslado").send({
				"text": json.dumps ({
					"exito": "V",
					"tipo":"Traslado aceptado",
					"principal": "Su traslado ha sido aceptado correctamente",
					"secundario":"recibido por:"+comentario,
					"usuario":str(TA.solicita.id),
					"ruta":"/bodega/traslados/ok/"
				})
			})
		pt = TRASLADO.objects.filter(no=TA.no).filter(numero=TA.indice)
		tienda=TA.no.a
		t2=TA.no.de
		for p in pt:
			sumar_inv = INVENTARIO.objects.filter(producto=p.producto).filter(tienda=tienda)
			restar_inv=INVENTARIO.objects.filter(producto=p.producto).filter(tienda=t2)
		
			if restar_inv.exists():
				restar_inv=restar_inv[0]
				ttl=p.cantidad
				if sumar_inv.exists():
					print "existe"
					sumar_inv=sumar_inv[0]
					sica =int(sumar_inv.cantidad)+ttl
					print sica
					sumar_inv.cantidad=sica
					sumar_inv.save()
				else:
					sumar_inv=INVENTARIO()
					sumar_inv.producto=p.producto
					sumar_inv.tienda=tienda
					sumar_inv.cantidad=ttl
					sumar_inv.costo=restar_inv.costo
					sumar_inv.distribuidor=restar_inv.distribuidor
					sumar_inv.mayorista=restar_inv.mayorista
					sumar_inv.efectivo=restar_inv.efectivo
					sumar_inv.tarjeta=restar_inv.tarjeta
					print "este no"
					sumar_inv.save()
				restar_inv.cantidad=restar_inv.cantidad-ttl
				restar_inv.save()


	else:
		TA.save()
		if reply_channel is not None:
			Group("traslado").send({
				"text": json.dumps ({
					"exito": "V",
					"tipo":"Traslado Rechazado",
					"principal": "Traslado rechazado:",
					"secundario":"motivo:"+comentario,
					"usuario":str(TA.solicita.id),
					"ruta":"/bodega/traslados/ok/"
				})
			})



@app.task
def limpiar_traslados_tienda(empresa):
	e=EMPRESA.objects.get(id=empresa)
	alerta = ALERTA.objects.filter(mensaje__icontains="traslado").filter(tienda=empresa)
	for a in alerta:
		a.visto=True
		a.save()


@app.task
def solicitud_de_traslado(de,a,usuario,reply_channel):
	nt = NO_TRASLADO.objects.filter(de=de).filter(a=a)
	if nt.exists():
		nt=nt[0]
		tr = TRASLADO.objects.filter(no=nt).filter(numero=nt.numero)
		if tr.exists():
			ta=TRASLADO_AUTORIZADO.objects.filter(no=nt).filter(indice=nt.numero)
			if ta.exists():
				if reply_channel is not None:
					Group("traslado").send({
						"text": json.dumps ({
							"exito": "F",
							"tipo":"Error al enviar",
							"principal": "Este traslado ya fue notificado",
							"usuario":usuario,
							"ruta":"/bodega/traslados/generar/"
						})
					})
			else:
				usu = Perfil.objects.get(id=usuario)
				ta=TRASLADO_AUTORIZADO()
				ta.no=nt
				ta.indice=nt.numero
				ta.solicita=usu
				ta.save()
				nt.numero=nt.numero+1
				nt.save()
				pr = Perfil.objects.filter(tienda=de).filter(puesto__nombre__icontains="BOD")
				alerta = ALERTA()
				alerta.tipo = 0
				alerta.mensaje="Solicitud de traslado"
				username_id=Perfil.objects.get(id=usuario)
				alerta.sub_mensaje="por "+str(username_id.usuario)
				alerta.requiere=username_id
				alerta.ruta = "/bodega/traslados/autorizar/"
				puesto = PUESTO.objects.filter(nombre__icontains="BOD")
				puesto=puesto[0]
				alerta.puesto = puesto
				alerta.tienda =EMPRESA.objects.get(id=de)
				alerta.save()
				for p in pr:
					if reply_channel is not None:
						Group("traslado").send({
							"text": json.dumps ({
								"exito": "V",
								"tipo":"Nuevo Traslado",
								"principal": str(usu)+" solicita autorizacion de un traslado",
								"usuario":p.id,
								"ruta":"/bodega/traslados/autorizar/"
							})
						})	

		else:
			if reply_channel is not None:
				Group("traslado").send({
					"text": json.dumps ({
						"exito": "F",
						"tipo":"Error al enviar",
						"principal": "La lista parece estar vacia",
						"usuario":usuario,
						"ruta":"/bodega/traslados/generar/"
					})
				})

