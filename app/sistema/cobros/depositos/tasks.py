from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from software_RST.settings.celery import app
from channels import Group

from .models import DEPOSITOS
from channels import Channel

from ....bancos.banco.models import CUENTA_BANCARIA
from .models import DEPOSITOS

import json

@app.task
def autorizar_deposito_cuentas(no,reply_channel):
	deposito = DEPOSITOS.objects.get(id=no)
	para= deposito.cuenta_acreditada
	para.capital=para.capital+deposito.monto
	para.save()
	deposito.visto=True
	deposito.save()
	if reply_channel is not None:
		Group("alertas").send({
			"text": json.dumps ({
				"exito": "V",
				"tipo":"depositoR",
				"principal": str(deposito.cuenta_acreditada.administra),
				"instruccion":"deposito recibido ",
				"solicita":str(deposito.cuenta_debitada.administra.id),
				"puesto":str(deposito.cuenta_debitada.administra.puesto.nombre),
				"ruta":"/caja/depositos"
			})
		})


@app.task
def descartar_deposito_cuentas(no,reply_channel):
	deposito = DEPOSITOS.objects.get(id=no)
	de= deposito.cuenta_debitada
	de.capital=de.capital+deposito.monto
	de.save()
	deposito.visto=True
	deposito.save()
	if reply_channel is not None:
		Group("alertas").send({
			"text": json.dumps ({
				"exito": "V",
				"tipo":"depositoE",
				"principal": str(deposito.cuenta_acreditada.administra)+" no recibio ",
				"instruccion":"la transferencia por "+str(deposito.monto)+" favor revisar",
				"solicita":str(de.administra.id),
				"puesto":str(de.administra.puesto.nombre),
				"ruta":"/caja/depositos"
			})
		})




@app.task
def realizar_deposito_cuentas(de,para,monto,documento,reply_channel):
	de=CUENTA_BANCARIA.objects.get(id=de)
	para=CUENTA_BANCARIA.objects.get(id=para)
	monto=float(monto)
	cap= float(de.capital)
	res= cap-monto
	if res>=0:
		de.capital=float(de.capital)-monto
		de.save()
		dep = DEPOSITOS()
		dep.cuenta_debitada= de
		dep.cuenta_acreditada=para
		dep.monto = monto
		dep.documento=documento
		dep.save()
		if reply_channel is not None:
			Group("alertas").send({
				"text": json.dumps ({
					"exito": "V",
					"tipo":"deposito",
					"principal": "El usuario "+str(de.administra)+" hizo una transferencia",
					"instruccion":"por "+str(monto)+" a la cuenta "+str(de.numero_de_cuenta),
					"solicita":str(para.administra.id),
					"puesto":str(para.administra.puesto.nombre),
					"ruta":"/caja/depositos/confirmar"
				})
			})
	else:
		if reply_channel is not None:
			Group("alertas").send({
				"text": json.dumps ({
					"exito": "V",
					"tipo":"fracaso",
					"principal": "Monto no valido",
					"instruccion":"favor revisar",
					"solicita":str(de.administra.id),
					"puesto":str(de.administra.puesto.nombre),
					"ruta":"/caja/depositos/"
				})
			})

	