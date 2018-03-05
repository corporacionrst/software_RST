from django.conf.urls import include, url


from .views  import *
	

urlpatterns = [
	url(r'^$',menu.as_view(),name='menu'),
	url(r'(?P<id>\d+)/$', modificar.as_view(), name='modificar'),
	
]


