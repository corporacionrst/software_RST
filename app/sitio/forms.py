from django import forms


class LoginForm(forms.Form):
	username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Usuario'}))
	password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}))
	
class formulario_permisos(forms.Form):
	de = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'yyyy-mm-dd',"type":"date"}))
	a  = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'yyyy-mm-dd',"type":"date"}))
	motivo = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'vacaciones'}))
	