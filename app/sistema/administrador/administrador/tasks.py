
from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from software_RST.settings.celery import app
from channels import Group
from channels import Channel

from django.db.models import Q
from ....alertas.models import ALERTA

from datetime import date

import json


import csv
import codecs


@app.task
def pedir_permiso_documento(usuario,reply_channel):
	try:
		usu = Prefil.objects.get(id=usuario)
		tienda=usu.tienda
		alerta=ALERTA()
		alerta.tipo=0
		mensaje="solicitud de autorizacion"
		subm="factura credito"
		alerta.mensaje=mensaje
		alerta.sub_mensaje=subm
		alerta.requiere=usu
		alerta.ruta=ruta
		alerta.puesto=Puesto.objects.filter(nombre__icontains="ADMIN")[0]
		alerta.tienda=tienda
		alerta.save()
		if reply_channel is not None:
			Group("alertas").send({
				"text": json.dumps ({
					"exito": "V",
					"tipo":"notificacion",
					"principal": mensaje,
					"instruccion":subm,
					"solicita":usu.username,
					"ruta":"/caja/cobros/permiso"
				})
			})
	except:
		print "algo salio mal"	



@task
def bg(csvfile):
	dialect = csv.Sniffer().sniff(codecs.EncodedFile(csvfile, "utf-8").read(1024))
	csvfile.open()
	reader = csv.reader(codecs.EncodedFile(csvfile, "utf-8"), delimiter=str(u','), dialect=dialect)
	for r in reader:
		print r
		print "\n\n\n\n\n"

@app.task
def cargar_marca(csvfile):
	dialect = csv.Sniffer().sniff(codecs.EncodedFile(csvfile, "utf-8").read(1024))
	csvfile.open()
	reader = csv.reader(codecs.EncodedFile(csvfile, "utf-8"), delimiter=str(u','), dialect=dialect)
	for r in reader:
		print r
		print "\n\n\n\n\n"


@app.task
def cargar_producto(csvfile):
	dialect = csv.Sniffer().sniff(codecs.EncodedFile(csvfile, "utf-8").read(1024))
	csvfile.open()
	reader = csv.reader(codecs.EncodedFile(csvfile, "utf-8"), delimiter=str(u','), dialect=dialect)
	for r in reader:
		print r
		print "\n\n\n\n\n"

@app.task
def cargar_clientes(csvfile):
	dialect = csv.Sniffer().sniff(codecs.EncodedFile(csvfile, "utf-8").read(1024))
	csvfile.open()
	reader = csv.reader(codecs.EncodedFile(csvfile, "utf-8"), delimiter=str(u','), dialect=dialect)
	for r in reader:
		print r
		print "\n\n\n\n\n"


@app.task
def cargar_inventario(csvfile):
	dialect = csv.Sniffer().sniff(codecs.EncodedFile(csvfile, "utf-8").read(1024))
	csvfile.open()
	reader = csv.reader(codecs.EncodedFile(csvfile, "utf-8"), delimiter=str(u','), dialect=dialect)
	for r in reader:
		print r
		print "\n\n\n\n\n"
			


			

	