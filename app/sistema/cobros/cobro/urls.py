from django.conf.urls import include, url


from .views  import *

urlpatterns = [
	url(r'^$',cobros.as_view(),name='menu'),
]
