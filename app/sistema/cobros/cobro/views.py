# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect

from django.views.generic import TemplateView

# Create your views here.

class cobros(TemplateView):
	def get(self,request,*args,**kwargs):
		return redirect("/")