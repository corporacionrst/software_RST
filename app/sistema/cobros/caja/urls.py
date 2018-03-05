from django.conf.urls import include, url


from .views  import *

urlpatterns = [
	url(r'^$',menu_cobros.as_view(),name='menu'),
	url(r'^contrasenas/',include("app.sistema.cobros.contrasena.urls",namespace="contrasena")),
	url(r'^depositos/',include("app.sistema.cobros.depositos.urls",namespace="depositos")),
	url(r'^cobros/',include("app.sistema.cobros.cobro.urls",namespace="cobros")),
	url(r'^cola/(?P<id>\d+)/$', factura.as_view(), name='factura'),
	url(r'^cola/$',cola.as_view(),name="cola"),
	url(r'^contado/',contado.as_view(),name="contado"),
	url(r'^credito/',credito.as_view(),name="credito"),
	url(r'^imprimir/',imprimir.as_view(),name="imprimir"),
	url(r'^recibos/',include("app.bancos.cuentas_por_cobrar.urls",namespace="recibos")),
	
	

]
