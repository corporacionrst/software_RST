from django.conf.urls import include, url


from .views import traslados

urlpatterns = [
	url(r'^$',traslados.as_view(),name="traslados"),
	]


