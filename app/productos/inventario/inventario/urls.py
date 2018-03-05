from django.conf.urls import include, url


from .views  import (
	inventario,
	local,
	cargar_a_lista,
	listar,
	quitar,
	total,
	inventario_local,
	info_detallada,
	consulta_pagina_tienda
)

urlpatterns = [
	url(r'^$',inventario.as_view(),name='in'),
	# url(r'^compras/',include("app.productos.inventario.compras.urls",namespace="tienda")),
	url(r'^local/',local.as_view(),name='local_inv'),
	url(r'^cargar_a_lista/',cargar_a_lista.as_view(),name='cargar_a_lista'),
	url(r'^listar/',listar.as_view(),name="listar"),
	url(r'^quitar/',quitar.as_view(),name="quitar"),
	url(r'^total/',total.as_view(),name="total"),
	url(r'^inventario_local',inventario_local.as_view(),name='inventario_local'),
	url(r'^(?P<id>\d+)/$', info_detallada.as_view(), name='info_detallada'),
	url(r'^consulta_pagina_tienda/',consulta_pagina_tienda.as_view(),name='consulta_pagina_tienda'),
    

]
