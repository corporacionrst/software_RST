# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from ....request_session import OKadmin,getPerfil

from .tasks import pedir_permiso_documento
from .forms import cargar_csv
from django.http import HttpResponse
import csv
import codecs

class excel(TemplateView):
	template_name="sistema/admin/excel.html"
	form_csv=cargar_csv
	initial={"key":"value"}
	def get(self,request,*args,**kwargs):
		if OKadmin(request):
			usu = getPerfil(request)
			context={
				"tienda":usu.tienda,
			}
			return render(request,self.template_name,context)
		return redirect("/")
	def post(self,request,*args,**kwargs):
		if request.POST and request.FILES:
			tipo = int(request.POST.get("opcion"))
			print tipo
			csvfile = request.FILES['csv_file']
			dialect = csv.Sniffer().sniff(codecs.EncodedFile(csvfile, "utf-8").read(1024))
			csvfile.open()
			reader = csv.reader(codecs.EncodedFile(csvfile, "utf-8"), delimiter=str(u','), dialect=dialect)
			print reader
			for r in reader:
				print r['marca']
				# print "\n\n\n\n\n"
			usu = getPerfil(request)
			context={
				"tienda":usu.tienda,
			}
    		return render(request, self.template_name, context)
		return redirect("/")

			

class admin(TemplateView):
	def get(self,request,*args,**kwargs):
		return redirect('/')

def pedir_permiso(usuario,reply_channel):
	task_id=pedir_permiso_documento.delay(usuario,reply_channel)
