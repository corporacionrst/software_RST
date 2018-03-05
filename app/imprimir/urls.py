from django.conf.urls import include, url

from .views  import factura

urlpatterns = [
	url(r'^(?P<id>\d+)/$',factura.as_view(),name='factura'),	
]
