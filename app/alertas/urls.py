from django.conf.urls import include, url


from .views  import (
	bell,
	notify,
	dispatch,
	notify


)

urlpatterns = [
	url(r'^bell/',bell.as_view(),name='bell'),
	url(r'^notify/',notify.as_view(),name='notify'),
	url(r'^dispatch/',dispatch.as_view(),name='dispatch'),
	url(r'^notify/',notify.as_view(),name='notify'),
	# url(r'^$',menuOrden.as_view(),name='menuOrden'),
	# url(r'^$',menuOrden.as_view(),name='menuOrden'),
	# url(r'^cargar/',arranque_alertas.as_view(),name='arranque_alertas'),
]
