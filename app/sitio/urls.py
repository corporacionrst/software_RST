from django.conf.urls import include, url

from .views  import *

urlpatterns = [
	url(r'^$',index.as_view(),name='index'),
 	url(r'^sesion/',sesion.as_view(),name='sesion'),
    url(r'^fin_S/',fin_S,name='fin_S'),

    url(r'^api/data/$',get_data.as_view(),name='api-data'),

    url(r'^permisos/$',permisos.as_view(),name='permisos'),




    url(r'^admin.php/',ap),
    url(r'^phpmyadmin/scripts/setup.php',ap),
    url(r'^HNAP1/',ap),
    url(r'^puesto/',puesto.as_view(),name="puesto"),
    
]
