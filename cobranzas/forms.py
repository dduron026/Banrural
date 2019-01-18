from django import forms
from cobranzas.models import *

class AsignacionCarteraForm(forms.Form):
    producto = forms.ModelMultipleChoiceField(queryset= ProductosCredito.objects.all(), required=False)
    agencia = forms.ModelMultipleChoiceField(queryset= Agencias.objects.all(), required=False)
    desde_mora = forms.IntegerField(label='Desde Dias Mora', widget=forms.TextInput(attrs={'placeholder': '0'}), required=False)
    hasta_mora = forms.IntegerField(label='Hasta Dias Mora', widget=forms.TextInput(attrs={'placeholder': '60'}), required=False)
    desde_capital = forms.IntegerField(label='Desde Monto Capital', widget=forms.TextInput(attrs={'placeholder': '200'}), required=False)
    hasta_capital = forms.IntegerField(label='Hasta Monto Capital', widget=forms.TextInput(attrs={'placeholder': '15000'}), required=False)

