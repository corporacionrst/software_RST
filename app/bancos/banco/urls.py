from django.conf.urls import include, url


from .views import menu_bancario,crear_banco,cuenta_bancos,asignar_cuenta_bancos

urlpatterns = [
	url(r'^$',menu_bancario.as_view(),name='menu_bancario'),
	url(r'^crear/',crear_banco.as_view(),name='crear_banco'),
	url(r'^crear_cuenta/',cuenta_bancos.as_view(),name='cuenta_bancos'),
	url(r'^asignar_cuenta/',asignar_cuenta_bancos.as_view(),name='asignar_cuenta_bancos'),
    
]
