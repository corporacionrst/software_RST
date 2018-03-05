from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from software_RST.settings.celery import app
from .models import PROVEEDOR
from ...sistema.tienda.models import EMPRESA
from ..persona.models import PERSONA
from channels import Channel
import json

@app.task
def crear_proveedor(nit,nombre,dirs,tel,mail,comm,credit,days,money,store,reply_channel):
	nit = nit.upper()
	nombre=nombre.upper()
	dirs=dirs.upper()
	tel=tel.upper()
	comm=comm.upper()
	exito="SI"
	if credit:
		cr="V"
	else:
		cr="F"
	mensaje=nit+" fue creado correctamente"
	try:
		persona = PERSONA.objects.get(nit=nit)
		prr=PROVEEDOR.objects.filter(info=persona).filter(store=store)
		if prr.exists():
			exito="NO"
			mensaje=nit+" ya existe"
			if prr.credito:
				cr="V"
			else:
				cr="F"
		else:
			prr= PROVEEDOR()
			prr.info=persona
			prr.comm=comm
			prr.credito=credit
			if money!=None and money!="":
				prr.monto=float(money)
			if days!=None and days !="":
				prr.dias_credito=int(days)
			prr.store=EMPRESA.objects.get(id=store)
			prr.save()
	except PERSONA.DoesNotExist:
		persona=PERSONA()
		persona.nit = nit
		persona.nombre= nombre
		persona.direccion= dirs
		persona.telefono= tel
		persona.correo=mail
		persona.save()
		prr=PROVEEDOR()
		prr.info=persona
		prr.comentario=comm
		prr.credito = credit
		if money!=None and money!="":
			prr.monto=float(money)
		if days!=None and days!="":
			prr.dias_credito = int(days)
		prr.store=EMPRESA.objects.get(id=store)
		prr.save()
		mensaje=nit+" fue creado correctamente"
	if reply_channel is not None:
		Channel(reply_channel).send({
				"text": json.dumps ({
				"exito": exito,
				"mensaje": mensaje,
				"nit":persona.nit,
				"nombre":persona.nombre,
				"direccion":persona.direccion,
				"credito":cr
			})
		})






	