from django.conf.urls import include, url


from .views  import *

urlpatterns = [
	url(r'^$',menu_proforma.as_view(),name='menu'),
	url(r'^generar/',generar.as_view(),name="generar"),


	url(r'^buscarProforma/',buscarProforma.as_view(),name="buscarProforma"),


	url(r'^ver/(?P<id>\d+)/$',vincular_pr.as_view(),name="vincular_pr"),

	url(r'^vincular/',vincular.as_view(),name="vincular"),
	

	url(r'^proforma/',proforma.as_view(),name="proforma"),
	

	url(r'^listar/$',listar_datos_factura.as_view(),name='listar_datos_factura'),
	url(r'^cargar_a_lista/$',cargar_a_lista_factura.as_view(),name='cargar_a_lista_factura'),
	url(r'^total/$',total_venta.as_view(),name="total_venta"),
	url(r'^quitar_prod/$',quitar_prod_factura.as_view(),name="quitar_prod_factura"),

	url(r'^imprimir/$',imprimir.as_view(),name="imprimir"),

	url(r'(?P<id>\d+)/$', factura.as_view(), name='proforma'),
	



]
