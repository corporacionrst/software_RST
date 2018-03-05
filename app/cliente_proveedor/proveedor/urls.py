from django.conf.urls import include, url


from .views  import (
	ver_proveedores,
	consultar_nit,
	consultar_nombre,
	registrar_proveedor,
)


urlpatterns = [
	url(r'^$',ver_proveedores.as_view(),name='ver_proveedores'),
	url(r'^nit/',consultar_nit.as_view(),name='consultar_nit_proveedor'),
	url(r'^nombre/',consultar_nombre.as_view(),name='consultar_nombre_proveedor'),
	url(r'^registrar_proveedor/',registrar_proveedor.as_view(),name='registrar_proveedor'),
	
]
