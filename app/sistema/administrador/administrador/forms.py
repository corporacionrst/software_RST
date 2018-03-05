from django import forms


BUSCAR_CSV=(('1','marca'),('2','productos'),('3','clientes'),('4','inventario'))

class cargar_csv(forms.Form):
	tipo = forms.ChoiceField(choices=BUSCAR_CSV)
	campo = forms.FileField()

