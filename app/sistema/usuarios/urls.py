from django.conf.urls import include, url


from .views import (
	usuarios,
	agregar_usuario,
	eliminar_usuario,
	historial,
	seguimiento
)

urlpatterns = [
	url(r'^$',usuarios.as_view(),name='usuarios'),
	url(r'^agregar/',agregar_usuario.as_view(),name='agregar_usuario'),
	url(r'^historial/(?P<id>\d+)/$',historial.as_view(),name="historial"),
	url(r'^eliminar/',eliminar_usuario.as_view(),name='eliminar_usuario'),
	url(r'^seguimiento/',seguimiento.as_view(),name='seguimiento'),


	

]
