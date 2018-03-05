from django.conf.urls import include, url


from .views  import (
	menu_facturacion,
	factura_no,
	registrar_venta,
	listar_datos_factura,
	cargar_a_lista_factura,
	consulta_inv,
	quitar_prod_factura,
	total_venta
	)

urlpatterns = [
	url(r'^$',menu_facturacion.as_view(),name='menu_facturacion'),
	url(r'(?P<id>\d+)/$', factura_no.as_view(), name='factura_no'),
	url(r'^registrar_venta/',registrar_venta.as_view(),name="registrar_venta"),
	

	url(r'^consulta_inv/',consulta_inv.as_view(),name="consulta_inv"),
	
	

	url(r'^listar/$',listar_datos_factura.as_view(),name='listar_datos_factura'),
	url(r'^cargar_a_lista/$',cargar_a_lista_factura.as_view(),name='cargar_a_lista_factura'),
	url(r'^total/$',total_venta.as_view(),name="total_venta"),
	url(r'^quitar_prod/$',quitar_prod_factura.as_view(),name="quitar_prod_factura"),

	url(r'^modificar/', include("app.sistema.ventas.modificar.urls",namespace="modificar")),
	


]


