from django.conf.urls import include, url

from .views  import (
	index_traslados,
	generar_traslado,
	tienda_trasladar,
	cargar_a_traslado,
	cargar_a_lista_traslado,
	quitar_lista_traslado,
	autorizar_traslados,
	traslados_vista_previa,
	recuperar,
	listar

	)

urlpatterns = [
	url(r'^$',index_traslados.as_view(),name='index'),
	url(r'^generar/$',generar_traslado.as_view(),name='generar'),
	url(r'^tienda/$',tienda_trasladar.as_view(),name='tienda_trasladar'),
	url(r'^cargar_a_traslado/$',cargar_a_traslado.as_view(),name='cargar_a_traslado'),
	url(r'^cargar_a_lista/$',cargar_a_lista_traslado.as_view(),name='cargar_a_lista_traslado'),
	url(r'^quitar/$',quitar_lista_traslado.as_view(),name='quitar_lista_traslado'),
	url(r'^autorizar/(?P<id>\d+)/$', traslados_vista_previa.as_view(), name='traslados_vista_previa'),
	url(r'^autorizar/$',autorizar_traslados.as_view(),name="autorizar"),
	url(r'^recuperar/$',recuperar.as_view(),name="recuperar"),
	url(r'^listar/$',listar.as_view(),name="listar"),
	
]
