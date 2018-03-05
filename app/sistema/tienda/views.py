from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from .forms import FormTienda,formCambiaTienda
from ...request_session import OKadmin,OKmultitienda
from django.http import HttpResponse,HttpResponseRedirect

from ..usuarios.models import Perfil,EMPRESA
from .converter import val_a_cad

class total_en_lentras(TemplateView):
	def get(self,request,*args,**kwargs):
		total=request.GET['total']
		moneda=request.GET['moneda']
		total_en_lentras=val_a_cad(total,moneda)
		return HttpResponse(total_en_lentras,content_type='text')

class tienda(TemplateView):
	template_name="sistema/admin/tienda/tienda.html"
	producto_form    = FormTienda
	tienda =formCambiaTienda
	initial = {'key': 'value'}

	def get(self, request, *args, **kwargs):
		if OKmultitienda(request):
			form = self.producto_form(initial=self.initial)
			ft = self.tienda(initial=self.initial)
			context ={
				"form":form,
				"tienda":ft,
			}
			return render(request, self.template_name, context)
		return redirect("/")

	def post(self,request,*args,**kwargs):
		if OKmultitienda(request):
			form = self.producto_form(request.POST)
			ft = self.tienda(initial=self.initial)
			context ={
				"form":form,
				"tienda":ft,
			}
			return render(request, self.template_name, context)
		return redirect("/")

class agregar_tienda(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKadmin(request):
			nombre=request.GET['nombre']
			addr=request.GET['addr']
			tel=request.GET['tel']
			admin=request.GET['admin']
			mp = EMPRESA()
			mp.nombre=nombre
			mp.direccion=addr
			mp.telefono=tel
			mp.save()
			prof=Perfil.objects.get(usuario=admin)
			prof.tienda=mp
			prof.save()
			return HttpResponse(nombre+" fue creada, administra:"+prof.username,content_type='text')

class refactorizar_tienda(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKmultitienda(request):
			try:
				tienda = request.GET['tienda']
				mp = EMPRESA.objects.get(id=tienda)
				rap = Perfil.objects.get(usuario=request.user)
				rap.tienda=mp
				rap.save()
				return HttpResponse("ahora operas en "+mp.nombre,content_type='text')
			except:
				return HttpResponse("Por favor, seleccione una tienda",content_type='text')




