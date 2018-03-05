from django import forms

from .models import MARCA

class MarcaForm(forms.ModelForm):
	class Meta:
		model=MARCA
		fields=[
			"nombre",
			"importacion",
		]