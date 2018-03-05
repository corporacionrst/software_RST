# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from ...request_session import OKbodega
from .forms import *
from .models import *


from django.views.generic import TemplateView



from .tasks import *
# Create your views here.
class ver_marca(TemplateView):
	template_name = 'productos/marca/ver.html'
	marca = MARCA
	def get(self,request,*args,**kwargs):
		if OKbodega(request):
			tabla= self.marca.objects.all().order_by('nombre')
			return render(request,self.template_name,{"tabla":tabla})
		return redirect("/")
		

	


# --------------------------crear marca--------------------------
class crear_marca(TemplateView):
	template_name = 'productos/marca/crear.html'
	marca_form    = MarcaForm
	initial = {'key': 'value'}

	def get(self, request, *args, **kwargs):
		if OKbodega(request):
			form = self.marca_form(initial=self.initial)
			context ={
				"form":form, 
				"realtime":"/rt",
			}
			return render(request, self.template_name, context)
		return redirect("/")
		

	def post(self,request,*args,**kwargs):
		if OKbodega(request):
			form = self.marca_form(request.POST)
			context ={
				"form":form, 
			}
			return render(request, self.template_name, context)
		return redirect("/")





# --------------------------modificar marca--------------------------
class modificar_marca(TemplateView):
	template_name = 'productos/marca/modificar.html'
	def get(self,request,*args,**kwargs):
		return render(request, self.template_name, {})

# --------------------------eliminar marca--------------------------
class eliminar_marca(TemplateView):
	template_name='productos/marca/eliminar.html'
	def get(self,request,*args,**kwargs):
		return render(request, self.template_name, {})

