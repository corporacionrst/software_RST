from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from software_RST.settings.celery import app
from channels import Group
from channels import Channel

import json
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse


from ..productos.inventario.historial.models import LISTA_PRODUCTO
from ..sistema.usuarios.models import Perfil,USUARIO_TIENDA,DOCUMENTO_POR_TIENDA


@app.task
def factura_a_pdf():
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="archivo.pdf"'

	buffer = BytesIO()

	# Create the PDF object, using the BytesIO object as its "file."
	p = canvas.Canvas(buffer)

	# Draw things on the PDF. Here's where the PDF generation happens.
	# See the ReportLab documentation for the full list of functionality.
	p.drawString(100, 100, "Hello world. biutiful")

	# Close the PDF object cleanly.
	p.showPage()
	p.save()

	# Get the value of the BytesIO buffer and write it to the response.
	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)
	print response



@app.task
def cargar_a_cola(indice,usu,reply_channel):
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
				Lista=LISTA_PRODUCTO.objects.filter(lista=dpt).filter(entregado__isnull=True)
				if Lista.exists():
					for l in Lista:
						if reply_channel is not None:
							Group("cola_socket").send({
								"text": json.dumps ({
									"tienda":l.lista.ubicado.tienda.id,
									"cantidad": l.cantidad,
									"producto": l.producto.codigo.nombre,
									"descripcion":l.producto.descripcion.detalle,
									"marca":l.producto.marca.nombre,
									"solicita":l.lista.ubicado.usuario.usuario.username,
									"id":l.id
								})
							})


