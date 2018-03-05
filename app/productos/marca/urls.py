from django.conf.urls import include, url

from .views  import *

urlpatterns = [
	url(r'^$',ver_marca.as_view(),name='ver'),
	url(r'^crear/',crear_marca.as_view(),name='crear')
    
]
