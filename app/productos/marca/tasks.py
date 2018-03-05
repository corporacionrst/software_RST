from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from software_RST.settings.celery import app

from .models import MARCA
from channels import Channel

import json

@app.task
def crear_marca_task(name2, importacion,reply_channel):
	name=str(name2).upper()
	brand = MARCA.objects.filter(nombre=name)
	creado="-"
	exito="SI"
	if brand.exists():
		creado=name +" ya existe"
		exito="NO"
	else:
		br = MARCA()
		br.nombre = name
		if len(name)<4:
			br.definicion=name
		else:
			br.definicion=name[0]+name[(len(name)-1)/2+1]+name[len(name)-1]
		br.importacion=importacion
		br.save()
		creado=name+" fue creado con exito"
	if reply_channel is not None:
		Channel(reply_channel).send({
				"text": json.dumps ({
				"exito": exito,
				"mensaje": creado,
			})
		})


	