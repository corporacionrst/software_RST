
from __future__ import unicode_literals
from django.db import models

from django.core.urlresolvers import reverse

class MARCA(models.Model):
	# TRANSLINK :True 
	# KOYO      :False
	nombre = models.CharField(max_length=20,primary_key=True)
	definicion=models.CharField(max_length=4,default="")
	importacion= models.BooleanField(default=False)
	def __unicode__(self):
		return unicode(self.nombre)
 	def url_absoluta(self):
		return reverse("productos:marca:crear")