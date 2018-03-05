from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from software_RST.settings.celery import app

from .models import Perfil,SALARIO_MENSUAL
from channels import Channel
from datetime import date,datetime

import json


@app.task
def consulta_usuario_fecha(desde,hasta,usuario,reply_channel):
	historial = Perfil.objects.get(id=usuario)
	if desde=="":
		desde= str(historial.ultima_indemnizacion)
	if hasta=="":
		hasta = str(datetime.now().year)+'-'+str(datetime.now().month)+'-'+str(datetime.now().day)
	
	retorno = SALARIO_MENSUAL.objects.filter(usuario=historial).filter(fecha_de_pago__gte=desde).filter(fecha_de_pago__lte=hasta)

	if reply_channel is not None:
			Channel(reply_channel).send({
					"text": json.dumps ({
					"tipo":"tabla",
					"fecha_de_pago": "<b>fecha de pago(yyyy-mm-dd)</b>",
					"salario":"<b>salario</b>",
					"comision":"<b>comisiones del mes</b>",
					"total" :"<b>total del mes</b>",
					"facturas_del_mes":"<b>facturas del mes</b>",

				})
			})
	for r in retorno:
		if reply_channel is not None:
			Channel(reply_channel).send({
					"text": json.dumps ({
					"tipo":"tabla",
					"fecha_de_pago": str(r.fecha_de_pago),
					"salario":str(r.salario),
					"comision":str(r.comision),
					"total" :str(r.total),
					"facturas_del_mes":"",

				})
			})



	