from django import forms

from ...tienda.models import EMPRESA

	
class FormDocumento(forms.Form):
	tienda = forms.ModelChoiceField(queryset=EMPRESA.objects.all().order_by('nombre'),widget=forms.Select(attrs={'class':'form-control dropdown-toggle','onchange':'cambio_tienda()'}))
	serie = forms.CharField(max_length=4,widget=forms.TextInput(attrs={'class':'form-control'}))
	documento = forms.IntegerField(required=False,widget=forms.TextInput(attrs={'class':'form-control','onkeypress':'return event.charCode>=48 && event.charCode<=57',"placeholder":"valor por defecto:1"}))