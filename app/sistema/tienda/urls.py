from django.conf.urls import include, url

from .views  import *

urlpatterns = [
	url(r'^$',tienda.as_view(),name='tienda'),
	url(r'^agregar/',agregar_tienda.as_view(),name='agregar_tienda'),
	url(r'^refactorizar/',refactorizar_tienda.as_view(),name='refactorizar_tienda'),
	url(r'^total_en_lentras/',total_en_lentras.as_view(),name='total_en_lentras')
    
]
