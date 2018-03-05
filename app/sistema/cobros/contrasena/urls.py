from django.conf.urls import include, url

from .views  import *

urlpatterns = [
	# url(r'^$',menu_cobros.as_view(),name='menu_cobros'),
	url(r'^$',lista_contrasena.as_view(),name="index"),
	url(r'^por_nit/',por_nit_contrasena.as_view(),name="por_nit_contrasena"),
	url(r'^cargar/$',cargar_a_contrasena.as_view(),name="cargar_a_contrasena"),
	url(r'^quitar/$',quitar_contrasena.as_view(),name="quitar_contrasena"),
	url(r'^lista_de_contrasena/',lista_de_contrasena.as_view(),name="lista_de_contrasena"),
	url(r'^imprimir/$',imprimir_contrasena.as_view(),name="imprimir_contrasena"),
	url(r'^(?P<id>\d+)/$', contrasena_impresa.as_view(), name='contrasena_impresa'),
	url(r'^showpasswd/$',showpasswd.as_view(),name="showpasswd"),
	



	# url(r'^contrasena/',include("app.sistema.cobros.contrasena.urls",namespace="contrasena")),
]
