from django.conf.urls import include, url


from .views  import *

urlpatterns = [
	url(r'^$',conta.as_view(),name='indice'),
	url(r'^documentos',documentos.as_view(),name="documentos"),
	url(r'^usuarios_por_tienda',usuarios_por_tienda.as_view(),name="usuarios_por_tienda"),
	
	
]
