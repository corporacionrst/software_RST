# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

class menu(TemplateView):
	template_name=""
	def get(self,request,*args,**kwargs):
		pass