
from django import forms
from .models import PUESTO
from django.forms.fields import DateField
from django.contrib.admin.widgets import AdminDateWidget 
from django.contrib.auth.forms import UserCreationForm



class crear_usuario(UserCreationForm):
	nombre=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'nombre'}))
	apellido=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'apellido'}))
	direccion=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'direccion'}))
	telefono=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'telefono'}))
	puesto=forms.ModelChoiceField(queryset=PUESTO.objects.all().order_by('nombre'),widget=forms.Select(attrs={'class':'form-control'}))
	fecha_de_nacimiento=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'yy-mm-dddd','type':'date'}))
	fecha_ingreso=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'yy-mm-dddd','type':'date'}))
	ultima_indmemnizacion=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'yy-mm-dddd','type':'date'}))
	cui_o_dpi=forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'dpi'}))
	numero_de_igss=forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'igss'}))
	salario_base=forms.CharField(required=False)
	