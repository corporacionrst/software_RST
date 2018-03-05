from django import forms

class FormPersona(forms.Form):
	nit = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control col-xl-6 col-lg-6 col-md-6',"onchange":"byNit()"}))
	nombre=forms.CharField(max_length=1000,widget=forms.TextInput(attrs={'class':'form-control col-xl-6 col-lg-6 col-md-6',"type":"search",'placeholder':'buscar por nombre','onkeyup':'count_nombre()','onkeydown':'endnombre()',}))
	direccion = forms.CharField(max_length=300,widget=forms.TextInput(attrs={'class':'form-control'}))
	credito= forms.BooleanField(required=False)
	


class Form_registrar(forms.Form):
	nit_a_registrar = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control col-xl-6 col-lg-6 col-md-6'}))
	nombre_a_registrar=forms.CharField(max_length=1000,widget=forms.TextInput(attrs={'class':'form-control col-xl-6 col-lg-6 col-md-6'}))
	direccion_a_registrar = forms.CharField(max_length=300,widget=forms.TextInput(attrs={'class':'form-control'}))
	ciudad = forms.BooleanField(required=False)
	es_set= forms.BooleanField(required=False)
	comentario= forms.CharField(required=False,max_length=300,widget=forms.TextInput(attrs={'class':'form-control'}))
	telefono_a_registrar = forms.CharField(required=False,max_length=300,widget=forms.TextInput(attrs={'class':'form-control'}))
	correo_a_registrar= forms.EmailField(required=False,max_length=300,widget=forms.TextInput(attrs={'class':'form-control','type':'email'}))
	credito_a_registrar= forms.BooleanField(required=False)
	monto_a_registrar=forms.CharField(required=False,max_length=300,widget=forms.TextInput(attrs={'class':'form-control','onkeypress':"return event.charCode>=48 && event.charCode<=57 || event.charCode==46"}))
	dias_de_credito_a_registrar=forms.CharField(required=False,max_length=300,widget=forms.TextInput(attrs={'class':'form-control','onkeypress':"return event.charCode>=48 && event.charCode<=57"}))
	