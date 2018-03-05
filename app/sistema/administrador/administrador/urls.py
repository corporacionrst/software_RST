from django.conf.urls import include, url


from .views import admin,excel

urlpatterns = [
	url(r'^$',admin.as_view(),name='admin'),
	url(r'^usuarios/',include("app.sistema.usuarios.urls",namespace="administrador_usuario")),
	url(r'^bancos/',include("app.bancos.banco.urls",namespace="banco")),
	url(r'^excel/',excel.as_view(),name="excel"),
	
]
