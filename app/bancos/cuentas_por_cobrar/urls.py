from django.conf.urls import include, url


from .views  import menu,pendientes,cola

urlpatterns = [
	url(r'^$',menu.as_view(),name='index'),
	url(r'^cola/',cola.as_view(),name="cola"),
	url(r'^pendientes/',pendientes.as_view(),name='pendientes'),
]
