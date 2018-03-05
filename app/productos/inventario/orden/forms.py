from django import forms


class Login_O_Form(forms.Form):
	nit=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'numero de nit'}))
	orden_de_compra=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'numero'}))
	