from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from software_RST.settings.celery import app

from ....productos.inventario.historial.models import LISTA_PRODUCTO
from ....productos.inventario.inventario.models import INVENTARIO

@app.task
def descargar_de_inventario(codigo_de_lista):
	lp = LISTA_PRODUCTO.objects.filter(lista__id=codigo_de_lista)
	for l in lp:
		inv = INVENTARIO.objects.filter(tienda=l.lista.ubicado.tienda).filter(producto=l.producto)
		if inv.exists():
			inv=inv[0]
			inv.cantidad=inv.cantidad-l.cantidad
			if l.unitario>inv.tarjeta:
				inv.tarjeta=l.unitario
			inv.save()
		else:
			print "LOG; ERRROOOOORRR"


	