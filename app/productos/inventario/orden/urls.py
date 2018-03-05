from django.conf.urls import include, url


from .views  import (
	menuOrden,
	cargar_orden_de_compra,
	ordenes_pendientes,
	cargar_listado_credito,
	cargar_listado_contado,
	ordenes_autorizadas,
	imprimir_orden,
	quitar,
	listar_datos_orden,
	cargar_a_lista_orden,
	total_orden,
	quitar_prod_oc,listar_compra,total_compra,quitar_prod_compra,cargar_a_lista_compra
	
)

urlpatterns = [
	url(r'^$',menuOrden.as_view(),name='menuOrden'),
	url(r'^cargar/',cargar_orden_de_compra.as_view(),name='cargar_orden_de_compra'),
	url(r'^pendientes/',ordenes_pendientes.as_view(),name='ordenes_pendientes'),
	url(r'^cargar_listado_credito/',cargar_listado_credito.as_view(),name='cargar_listado_creditoOC'),
	url(r'^cargar_listado_contado/',cargar_listado_contado.as_view(),name='cargar_listado_contadoOC'),
	url(r'^autorizadas/(?P<id>\d+)/$', imprimir_orden, name='imprimir_orden'),
	url(r'^autorizadas/$',ordenes_autorizadas.as_view(),name='ordenes_autorizadas'),
	url(r'^quitar/$',quitar.as_view(),name='quitar_ordenes_autorizadas'),


	url(r'^listar_compra/$',listar_compra.as_view(),name='listar_compra'),
	url(r'^cargar_a_lista_compra/$',cargar_a_lista_compra.as_view(),name='cargar_a_lista_compra'),	
	url(r'^total_compra/$',total_compra.as_view(),name="total_compra"),
	url(r'^quitar_prod_compra/$',quitar_prod_compra.as_view(),name="quitar_prod_compra"),


	url(r'^listar/$',listar_datos_orden.as_view(),name='listar_datos_orden'),
	url(r'^cargar_a_lista/$',cargar_a_lista_orden.as_view(),name='cargar_a_lista_orden'),
	url(r'^total/$',total_orden.as_view(),name="total_orden"),
	url(r'^quitar_prod/$',quitar_prod_oc.as_view(),name="quitar_prod_oc"),


	
	# listar
# autorizadas


]
