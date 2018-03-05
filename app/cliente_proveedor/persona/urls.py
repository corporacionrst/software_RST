from django.conf.urls import include, url


urlpatterns = [

	# url(r'^cliente/',include("app.cliente_proveedor.cliente.urls",namespace="clientes"),
	url(r'^proveedor/',include("app.cliente_proveedor.proveedor.urls",namespace="proveedor"),
	
]
