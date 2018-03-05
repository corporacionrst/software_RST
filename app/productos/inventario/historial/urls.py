from django.conf.urls import include, url

from .views  import listar_producto

urlpatterns = [
	url(r'^listar_producto/',listar_producto.as_view(),name='listar_producto'),
	
]
