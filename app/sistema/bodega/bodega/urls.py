from django.conf.urls import include, url

from .views  import *

urlpatterns = [
	url(r'^$',bodega_index.as_view(),name='index'),
	url(r'^traslados/',include("app.sistema.bodega.traslados.urls",namespace="traslados")),
	url(r'^cola/$',cola.as_view(),name='cola'),
	url(r'^quitar/$',quitar.as_view(),name='quitar'),
	url(r'^lista/$',lista.as_view(),name='lista'),
	url(r'^faltantes/(?P<id>\d+)/',id_faltantes.as_view(),name='id_faltantes'),
	url(r'^faltantes/$',faltantes.as_view(),name='faltantes'),
	
	

]
