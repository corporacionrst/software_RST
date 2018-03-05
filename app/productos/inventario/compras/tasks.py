from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from software_RST.settings.celery import app

from channels import Channel
import json
from django.db.models import Q

from django.utils.dateparse import parse_date
from ....cliente_proveedor.persona.models import PERSONA
from ....cliente_proveedor.proveedor.models import PROVEEDOR
from ....sistema.usuarios.models import Perfil,DOCUMENTO_POR_TIENDA
from ..historial.models import HISTORIAL,LISTA_PRODUCTO
from ....factores import *

from ..inventario.models import INVENTARIO


@app.task
def historial_compras(doc,nnit,credito,info,fecha):
	nit = PERSONA.objects.get(nit=nnit)
	his = HISTORIAL.objects.filter(documento=doc).filter(cliente_proveedor=nit).filter(lista__tipo_doc="C")
	dpt = DOCUMENTO_POR_TIENDA.objects.get(id=info)
	if not his.exists():
		if credito:
			proveedor=PROVEEDOR.objects.filter(info=nit).filter(store=dpt.ubicado.tienda)[0]
			dpt.credito=credito
			dpt.save()
			proveedor.saldo=proveedor.saldo+dpt.total
			proveedor.save()
		his = HISTORIAL()
		his.documento = doc
		his.cliente_proveedor= nit
		his.fehca_registro =  parse_date(fecha)
		his.ingresa= dpt.ubicado.usuario
		his.lista=dpt
		his.save()
		lp = LISTA_PRODUCTO.objects.filter(lista=dpt)
		for l in lp:
			prod = INVENTARIO.objects.filter(tienda=dpt.ubicado.tienda).filter(producto=l.producto)
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
				prod.tienda= dpt.ubicado.tienda
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











	