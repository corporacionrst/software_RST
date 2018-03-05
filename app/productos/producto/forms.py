from django import forms

from .models import *
from ..marca.models import MARCA


class FormProducto(forms.Form):
	codigo= forms.CharField(max_length=300,widget=forms.TextInput(attrs={'class':'form-control'}))
	descripcion=forms.CharField(max_length=1000,widget=forms.TextInput(attrs={'class':'form-control'}))
	marca = forms.ModelChoiceField(queryset=MARCA.objects.all().order_by('nombre'),widget=forms.Select(attrs={'class':'form-control dropdown-toggle'}))
	es_set = forms.BooleanField(required=False)
