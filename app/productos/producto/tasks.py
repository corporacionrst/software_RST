from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from software_RST.settings.celery import app

from .models import *
from ..marca.models import MARCA
from channels import Channel

import json

@app.task
def crear_producto_task(codigo,descripcion,marca,set_ID,numero_set,reply_channel):
	info_codigo = str(codigo).upper()
	info_descripcion=str(descripcion).upper()
	code = CODIGO.objects.filter(nombre=info_codigo)
	if not code.exists():
		code = CODIGO()
		code.nombre=info_codigo
		code.save()
	detail= DESCRIPCION.objects.filter(detalle=info_descripcion)
	if not detail.exists() and info_descripcion is not "":
		detail=DESCRIPCION()
		detail.detalle=info_descripcion
		detail.save()
	check_marca=MARCA.objects.get(nombre=marca)
	pr = PRODUCTO.objects.filter(codigo=code).filter(marca=check_marca)
	exito =""
	creado=""
	suma=""
	if not pr.exists():
		exito="SI"
		creado=info_codigo+ " fue creado con exito"
		pr=PRODUCTO()
		pr.codigo = CODIGO.objects.get(nombre=info_codigo)
		pr.descripcion = DESCRIPCION.objects.get(detalle=info_descripcion)
		pr.marca = MARCA.objects.get(nombre=marca)
		if set_ID:
			suma="SI"
			id_set=SET.objects.get(numero=numero_set)
			pr.id_set=id_set
		pr.save()
	else:
		exito="NO"
		creado=info_codigo +" ya existe"
	if reply_channel is not None:
		Channel(reply_channel).send({
				"text": json.dumps ({
				"exito": exito,
				"mensaje": creado,
				"suma":suma
			})
		})




	