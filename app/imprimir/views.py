# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.views.generic import TemplateView

from reportlab.pdfgen import canvas

from django.http import HttpResponse
from io import BytesIO

from reportlab.pdfgen import canvas
from django.http import HttpResponse

from .tasks import factura_a_pdf

class factura(TemplateView):
	template_name="impresion/documento.html"
	def get(self,request,id=None,*args,**kwargs):
		fap = factura_a_pdf.delay()
		return render(request,self.template_name)
		