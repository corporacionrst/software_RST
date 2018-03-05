
from django.conf.urls import include, url


from .views  import (
	ver_clientes,
	consultar_cliente_nit,
	consultar_cliente_nombre,
	registrar_cliente,
	mayorista,
	descuento,
)

urlpatterns = [
	url(r'^$',ver_clientes.as_view(),name='ver_clientes'),
	url(r'^nit/$',consultar_cliente_nit.as_view(),name='consultar_nit'),
	url(r'^nombre/$',consultar_cliente_nombre.as_view(),name='consultar_nombre'),
	url(r'^registrar_cliente/$',registrar_cliente.as_view(),name='registrar_cliente'),
	url(r'^mayorista/$',mayorista.as_view(),name='mayorista'),
	url(r'^descuento/$',descuento.as_view(),name='descuento'),
	
	
]
