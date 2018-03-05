from django.conf.urls import include, url


from .views  import (
	crear_producto,
	consulta_pagina,
	cargar_set,
	tabla_set,
	consulta_pagina_set,
	quitar_set,
	sumar_d3,
	set_producto,
	obtener_producto,
	asignar_set,
	)

urlpatterns = [
	
	url(r'^crear/$',crear_producto.as_view(),name='crear'),
	url(r'^marca/', include("app.productos.marca.urls",namespace="marca")),
    url(r'^consulta_pagina/',consulta_pagina.as_view(),name='consulta_pagina'),
    url(r'^consulta_pagina_set/',consulta_pagina_set.as_view(),name='consulta_pagina_set'),
   
    # SET
    url(r'^cargar_set/',cargar_set.as_view(),name='cargar_set'),
    url(r'^tabla_set/',tabla_set.as_view(),name='tabla_set'),
    url(r'^quitar_set/',quitar_set.as_view(),name='quitar_set'),
	url(r'^sumar_d3/',sumar_d3.as_view(),name='sumar_d3'),

	url(r'^set/',set_producto.as_view(),name='set'),

	url(r'^obtener/',obtener_producto.as_view(),name='obtener_producto'),

	url(r'^asignar_set/',asignar_set.as_view(),name='asignar_set'),

	url(r'^traslados/',include("app.productos.inventario.traslado.urls",namespace="traslado")),

	url(r'^compras/',include("app.productos.inventario.compras.urls",namespace="compras")),

	url(r'^inventario/',include("app.productos.inventario.inventario.urls",namespace="inventario")),

	url(r'^orden_de_compra/',include("app.productos.inventario.orden.urls",namespace="orden")),
	
    
]


