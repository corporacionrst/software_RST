from django.conf.urls import include, url


from .views  import (
	inv_local,
	ver_compras,
	cargar_factura,
	registrar_compra,
	documento,
	detallar_compra

)

urlpatterns = [
	url(r'^local/',inv_local.as_view(),name='inv_local'),
	url(r'^$',ver_compras.as_view(),name='ver'),
	url(r'^cargar/',cargar_factura.as_view(),name='cargar_factura'),
	url(r'^registrar_compra/',registrar_compra.as_view(),name="registrar_compra"),
	url(r'^documento/',documento.as_view(),name='documento_compras'),
    url(r'^detallar_compra/',detallar_compra.as_view(),name="detallar_compra"),

	
]
