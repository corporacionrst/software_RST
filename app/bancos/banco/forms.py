from django import forms

from models import CUENTA_BANCARIA,BANCO


class BancoForm(forms.Form):
	banco = forms.CharField(max_length=300,widget=forms.TextInput(attrs={'class':'form-control'}))

class AsignaBanco(forms.Form):
	banco = forms.ModelChoiceField(queryset=BANCO.objects.all().order_by('nombre'),widget=forms.Select(attrs={'class':'form-control dropdown-toggle'}))
	numero = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	monto = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','onkeypress':'return event.charCode>=48 && event.charCode<=57 || event.charCode==46'}))
	
	