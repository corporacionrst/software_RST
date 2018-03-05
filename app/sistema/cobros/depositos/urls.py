from django.conf.urls import include, url


from .views import (hacer_depositos,
	confirmar_depositos,
	cola_depositos,
	)

urlpatterns = [
	url(r'^$',hacer_depositos.as_view(),name='hacer_depositos'),
	url(r'^confirmar/',confirmar_depositos.as_view(),name='confirmar_depositos'),
	url(r'^cola/',cola_depositos.as_view(),name='cola_depositos'),


	
	
]
