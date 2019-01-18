# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.forms.widgets import *
from django import forms
from cliente.models import *
from django.contrib.auth.models import User

from django.utils.safestring import mark_safe

GENERO = (
	(1, "Hombre"),
	(2, "Mujer"),
)

ESTADO_CIVIL = (
	(1, "Soltero(a)"),
	(2, "Casado(a)"),
	(3, "Union Libre"),
	(4, "Viudo(a)"),
)

INGRESOS = (
	(1, "Menos de L 8000.00"),
	(2, "De L.8000.01 a L.10,000.00"),
	(3, "De L.10,000.01 a L.20,000.00"),
	(4, "De L.20,000.01 en adelante"),
	(5, "No Contestó"),
)
class ClienteActualizarForm(ModelForm):
	class Meta:
		model = ClienteActualizar
		fields = "__all__"
		exclude = ['actualizado', 'codigo','actualizado_por', 'con_coopcel', 'municipio', 'profesion', 'municipio_trabajo', 'fecha_actualizacion', 'sucursal', 'agente', 'identidad', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'sexo']
	 	widgets = {
	 		'identidad': TextInput(attrs={'readonly': 'readonly', 'type': 'text'}),
	 		'referencia': TextInput(attrs={'required': 'required'}),
	 	}
	ingresos =  forms.ChoiceField(choices=INGRESOS, widget=RadioSelect, required=False, initial=None)
	estado_civil =  forms.ChoiceField(choices=ESTADO_CIVIL, widget=RadioSelect, initial=None, label='Estado Civil*')

class ClienteGeneralForm(ModelForm):
	class Meta:
		model = ClienteActualizar
		fields = "__all__"
		exclude = ['actualizado', 'codigo','actualizado_por', 'con_coopcel', 'municipio', 'profesion', 'municipio_trabajo', 'fecha_actualizacion', 'sucursal', 'agente', 'identidad', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'sexo']
	 	widgets = {
	 		'identidad': TextInput(attrs={'readonly': 'readonly', 'type': 'text'}),
	 	}
	ingresos =  forms.ChoiceField(choices=INGRESOS, widget=RadioSelect, required=False, initial=None)
	estado_civil =  forms.ChoiceField(choices=ESTADO_CIVIL, widget=RadioSelect, initial=None)


class ClienteForm(ModelForm):
	class Meta:
		model = Cliente
		fields = "__all__"
		exclude = ['actualizado', 'codigo','actualizado_por', 'con_coopcel', 'municipio', 'profesion', 'municipio_trabajo', 'fecha_actualizacion', 'sucursal', 'agente', 'identidad', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'sexo']




class ClienteHistoricoForm(ModelForm):
	class Meta:
		model = ClienteHistorico
		fields = ['telefono_celular2', 'rifa', 'puesto', 'codigo','con_coopcel','tipo_empresa', 'correo_electronico', 'profesion_cliente', 'antiguedad_meses', 'actividad_cliente', 'antiguedad_anios', ]	
