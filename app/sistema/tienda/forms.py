from django import forms

from .models import *
from ...sistema.usuarios.models import *
from django.db.models import Q


class FormTienda(forms.Form):
	nombre= forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'form-control'}))
	direccion=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
	telefono=forms.CharField(max_length=15,widget=forms.TextInput(attrs={'class':'form-control'}))
	admin=forms.ModelChoiceField(queryset=Perfil.objects.filter(Q(puesto__nombre__icontains="AD")).order_by('usuario__username'),widget=forms.Select(attrs={'class':'form-control'}))
	
class formCambiaTienda(forms.Form):
	tienda = forms.ModelChoiceField(queryset=EMPRESA.objects.all().order_by('nombre'),widget=forms.Select(attrs={'class':'form-control'}))