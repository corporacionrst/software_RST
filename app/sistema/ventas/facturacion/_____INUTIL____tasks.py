from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from software_RST.settings.celery import app
from channels import Group
from channels import Channel

from django.db.models import Q


from datetime import date

from ...usuarios.models import Perfil,USUARIO_TIENDA,DOCUMENTO_POR_TIENDA
from ....productos.inventario.historial.models import LISTA_PRODUCTO

import json

@app.task
def cargar_a_cola_task(indice,usu,reply_channel):
	print "hola?"
	if indice<5 and indice>0:
		perfil = Perfil.objects.filter(usuario__id=usu)[0]
		ut = USUARIO_TIENDA.objects.filter(usuario=perfil).filter(tienda=perfil.tienda)
		if ut.exists():
			ut=ut[0]
			correlativo=0
			if indice==1:
				correlativo=ut.fac_1
			elif indice==2:
				correlativo=ut.fac_2
			elif indice==3:
				correlativo=ut.fac_3
			else:
				correlativo=ut.fac_4
			dpt =DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=indice).filter(correlativo=correlativo).filter(tipo_doc="V")
			if dpt.exists():
				dpt=dpt[0]
				i=int(request.GET["pag"])*5
				Lista=LISTA_PRODUCTO.objects.filter(lista=dpt)
				if Lista.exists():
					for l in Lista:
						if reply_channel is not None:
							Group("alertas").send({
								"text": json.dumps ({
									"tienda":l.lista.ubicado.tienda.id,
									"cantidad": l.cantidad,
									"producto": l.producto.codigo+"__"+l.producto.descripcion,
									"marca":l.producto.marca,
									"solicita":l.lista.ubicado.usuario.username,
									"id":l.id
								})
							})
			print "enviado a bodega correctamente"
				
