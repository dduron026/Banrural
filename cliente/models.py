# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from general.models import *

GENERO = (
	(1, "Hombre"),
	(2, "Mujer"),
)


class ActividadEconomica(models.Model):
    codigo_actividad_economica = models.AutoField(db_column='CODIGO_ACTIVIDAD_ECONOMICA',primary_key=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='DESCRIPCION', max_length=60, blank=True, null=True)  # Field name made lowercase.
    activo_b = models.CharField(db_column='ACTIVO_B', max_length=1, blank=True, null=True)  # Field name made lowercase.
    creado_por = models.CharField(db_column='CREADO_POR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fecha_creacion = models.CharField(db_column='FECHA_CREACION', max_length=27, blank=True, null=True)  # Field name made lowercase.
    modificado_por = models.CharField(db_column='MODIFICADO_POR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fecha_modificacion = models.CharField(db_column='FECHA_MODIFICACION', max_length=27, blank=True, null=True)  # Field name made lowercase.

    class Meta:
    	managed = False
        db_table = 'ACTIVIDADES_ECONOMICAS'

    def __unicode__(self):
		return self.descripcion

class Profesion(models.Model):
    codigo_profesion = models.AutoField(db_column='CODIGO_PROFESION',primary_key=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='DESCRIPCION', max_length=60, blank=True, null=True)  # Field name made lowercase.
    activo_b = models.CharField(db_column='ACTIVO_B', max_length=1, blank=True, null=True)  # Field name made lowercase.
    creado_por = models.CharField(db_column='CREADO_POR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fecha_creacion = models.DateTimeField(db_column='FECHA_CREACION', blank=True, null=True)  # Field name made lowercase.
    modificado_por = models.CharField(db_column='MODIFICADO_POR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fecha_modificacion = models.DateTimeField(db_column='FECHA_MODIFICACION', blank=True, null=True)  # Field name made lowercase.

    class Meta:
    	managed = False
        db_table = 'PROFESIONES'

    def __unicode__(self):
		return self.descripcion


class Cliente(models.Model):
	codigo = models.CharField(db_column='CodCliente', max_length=100)
	identidad = models.CharField(db_column='Identidad', max_length=20)
	primer_nombre = models.CharField(db_column='PrimerNombre', max_length=255)
	segundo_apellido = models.CharField(db_column='SegundoApellido', max_length=255, blank=True, null=True)
	primer_apellido = models.CharField(db_column='PrimerApellido', max_length=255)
	sexo = models.IntegerField(db_column='Sexo', choices=GENERO)
	estado_civil = models.IntegerField(db_column='EstadoCivil', blank=True, null=True)
	departamento = models.ForeignKey(Departamento, db_column='Departamento', blank=True, null=True, related_name='departamento_propio')
	municipio = models.ForeignKey(Municipio, db_column='Municipio', blank=True, null=True, related_name='municipio_propio', verbose_name='Municipio*')
	colonia = models.CharField(db_column='Colonia', max_length=150, blank=True, null=True)
	referencia = models.CharField(db_column='Referencia', max_length=1000, blank=True, null=True)
	telefono_fijo = models.CharField(db_column='TelefonoFijo', max_length=12, blank=True, null=True)
	telefono_celular = models.CharField(db_column='TelefonoCelular', max_length=12, blank=True, null=True)
	correo_electronico = models.CharField(db_column='CorreoElectronico', max_length=100, blank=True, null=True)
	profesion = models.CharField(db_column='Profesion', max_length=255, blank=True, null=True)
	ingresos = models.FloatField(db_column='Ingresos', blank=True, null=True)
	monto_cuentas = models.FloatField(db_column='MontoCuentas', blank=True, null=True)
	departamento_trabajo = models.ForeignKey(Departamento, db_column='DepartamentoTrabajo', blank=True, null=True, related_name='departamento_trabajo')
	municipio_trabajo = models.ForeignKey(Municipio, db_column='MunicipioTrabajo', blank=True, null=True, related_name='municipio_trabajo')
	lugar_trabajo = models.CharField(db_column='LugarTrabajo', max_length=255, blank=True, null=True)
	referencia_trabajo = models.CharField(db_column='ReferenciaTrabajo', max_length=1000, blank=True, null=True)
	telefono_fijo_trabajo = models.CharField(db_column='TelefonoFijoTrabajo', max_length=12, blank=True, null=True)
	correo_electronico_trabajo = models.CharField(db_column='CorreoElectronicoTrabajo', max_length=100, blank=True, null=True)
	actualizado = models.BooleanField(db_column='Actualizado', default=False)
	sucursal = models.ForeignKey(Sucursal, db_column='Sucursal', max_length=255, blank=True, null=True)
	agente = models.ForeignKey(User, db_column='Agente', null=True, blank=True, related_name='sucursal_cliente')
	filial =  models.ForeignKey(Filial, db_column='Filial', blank=True, null=True)
	actualizado_por = models.ForeignKey(User, db_column='ActualizadoPor', related_name='actualizado_por_clients')
	fecha_actualizacion = models.DateTimeField(db_column='FechaActualizacion', auto_now=True)
	codigo_rechazo = models.IntegerField(db_column='CodigoRechazo', blank=True, null=True)
	comentarios = models.CharField(db_column='Comentarios', max_length=155, blank=True, null=True)
	profesion_cliente = models.ForeignKey(Profesion, db_column='ProfesionCliente', blank=True, null=True, verbose_name='Profesión')
	actividad_cliente = models.ForeignKey(ActividadEconomica, db_column='ActividadCliente', blank=True, null=True, verbose_name='Rubro')
	con_coopcel = models.NullBooleanField(db_column='ConCoopcel', default=False)

	class Meta:
		db_table = 'Clientes'
	def __unicode__(self):
		return u'%s - %s %s %s %s' % (self.identidad, self.primer_nombre, self.segundo_apellido, self.primer_apellido, self.segundo_apellido)

class ClienteHistorico(models.Model):
	codigo = models.CharField(db_column='CodCliente', max_length=100)
	identidad = models.CharField(db_column='Identidad', max_length=20)
	primer_nombre = models.CharField(db_column='PrimerNombre', max_length=255)
	primer_apellido = models.CharField(db_column='PrimerApellido', max_length=255)
	segundo_apellido = models.CharField(db_column='SegundoApellido', max_length=255, blank=True, null=True)
	sexo = models.IntegerField(db_column='Sexo', choices=GENERO)
	estado_civil = models.IntegerField(db_column='EstadoCivil', blank=True, null=True)
	departamento = models.ForeignKey(Departamento, db_column='Departamento', blank=True, null=True, related_name='departamento_propio_his')
	municipio = models.ForeignKey(Municipio, db_column='Municipio', blank=True, null=True, related_name='municipio_propio_his')
	colonia = models.CharField(db_column='Colonia', max_length=150, blank=True, null=True)
	referencia = models.CharField(db_column='Referencia', max_length=1000, blank=True, null=True)
	telefono_fijo = models.CharField(db_column='TelefonoFijo', max_length=12, blank=True, null=True)
	telefono_celular = models.CharField(db_column='TelefonoCelular', max_length=12, blank=True, null=True)
	correo_electronico = models.CharField(db_column='CorreoElectronico', max_length=100, blank=True, null=True)
	profesion = models.CharField(db_column='Profesion', max_length=255, blank=True, null=True)
	ingresos = models.FloatField(db_column='Ingresos', blank=True, null=True)
	monto_cuentas = models.FloatField(db_column='MontoCuentas', blank=True, null=True)
	departamento_trabajo = models.ForeignKey(Departamento, db_column='DepartamentoTrabajo', blank=True, null=True, related_name='departamento_trabajo_his')
	municipio_trabajo = models.ForeignKey(Municipio, db_column='MunicipioTrabajo', blank=True, null=True, related_name='municipio_trabajo_his')
	lugar_trabajo = models.CharField(db_column='LugarTrabajo', max_length=255, blank=True, null=True)
	referencia_trabajo = models.CharField(db_column='ReferenciaTrabajo', max_length=1000, blank=True, null=True)
	telefono_fijo_trabajo = models.CharField(db_column='TelefonoFijoTrabajo', max_length=12, blank=True, null=True)
	correo_electronico_trabajo = models.CharField(db_column='CorreoElectronicoTrabajo', max_length=100, blank=True, null=True)
	actualizado = models.BooleanField(db_column='Actualizado', default=False)
	sucursal = models.ForeignKey(Sucursal, db_column='Sucursal', max_length=255, blank=True, null=True)
	agente = models.ForeignKey(User, db_column='Agente', null=True, blank=True, related_name='agente_historico')
	filial =  models.ForeignKey(Filial, db_column='Filial', blank=True, null=True)
	actualizado_por = models.ForeignKey(User, db_column='ActualizadoPor', related_name='actualizado_por_historico')
	modificado_por = models.ForeignKey(User, db_column='ModificadoPor', related_name='modificado_por_historico', blank=True, null=True)
	fecha_actualizacion = models.DateTimeField(db_column='FechaActualizacion', auto_now=True)
	codigo_rechazo = models.IntegerField(db_column='CodigoRechazo', blank=True, null=True)
	comentarios = models.CharField(db_column='Comentarios', max_length=155, blank=True, null=True)
	telefono_celular2 = models.CharField(db_column='TelefonoCelular2', max_length=12, blank=True, null=True)
	tipo_empresa = models.ForeignKey(TipoEmpresa,db_column='TipoEmpresa', blank=True, null=True, verbose_name='Tipo de Empresa*')
	puesto = models.CharField(db_column='Puesto', max_length=50, blank=True, null=True, verbose_name='Puesto/Cargo')
	antiguedad_anios = models.IntegerField(db_column='AntiguedadAnios', blank=True, null=True, verbose_name='Antiguedad Años')
	antiguedad_meses = models.IntegerField(db_column='AntiguedadMeses', blank=True, null=True, verbose_name='Antiguedad Meses')
	rifa = models.IntegerField(db_column='NumeroRifa', null=True, blank=True)
	profesion_cliente = models.ForeignKey(Profesion, db_column='ProfesionCliente', blank=True, null=True, verbose_name='Profesión')
	actividad_cliente = models.ForeignKey(ActividadEconomica, db_column='ActividadCliente', blank=True, null=True, verbose_name='Rubro')
	actualizado_core = models.NullBooleanField()
	con_coopcel = models.NullBooleanField(db_column='ConCoopcel', default=False)

	class Meta:
		db_table = 'ClientesHistoricos'

	def __unicode__(self):
		return u'%s - %s %s %s %s' % (self.identidad, self.primer_nombre, self.segundo_apellido, self.primer_apellido, self.segundo_apellido)

class ClienteActualizar(models.Model):
	codigo = models.CharField(db_column='CodCliente', max_length=100)
	identidad = models.CharField(db_column='Identidad', max_length=20)
	primer_nombre = models.CharField(db_column='PrimerNombre', max_length=255)
	primer_apellido = models.CharField(db_column='PrimerApellido', max_length=255)
	segundo_apellido = models.CharField(db_column='SegundoApellido', max_length=255, blank=True, null=True)
	sexo = models.IntegerField(db_column='Sexo', choices=GENERO)
	estado_civil = models.IntegerField(db_column='EstadoCivil', blank=True, null=True, verbose_name='Estado Civil*')
	departamento = models.ForeignKey(Departamento, db_column='Departamento', blank=True, null=True, related_name='departamento_propio_act', verbose_name='Departamento*')
	municipio = models.ForeignKey(Municipio, db_column='Municipio', blank=True, null=True, related_name='municipio_propio_act', verbose_name='Municipio*')
	colonia = models.CharField(db_column='Colonia', max_length=150, blank=True, null=True, verbose_name='Dirección Completa*')
	referencia = models.CharField(db_column='Referencia', max_length=1000, blank=True, null=True, verbose_name='Referencia*')
	telefono_fijo = models.CharField(db_column='TelefonoFijo', max_length=12, blank=True, null=True, verbose_name='Teléfono Fijo')
	telefono_celular = models.CharField(db_column='TelefonoCelular', max_length=12, blank=True, null=True)
	correo_electronico = models.CharField(db_column='CorreoElectronico', max_length=100, blank=True, null=True)
	profesion = models.CharField(db_column='Profesion', max_length=255, blank=True, null=True, verbose_name='Profesión u Oficio')
	ingresos = models.IntegerField(db_column='Ingresos', blank=True, null=True)
	monto_cuentas = models.FloatField(db_column='MontoCuentas', blank=True, null=True, verbose_name='Promedio de Ahorro Mensual')
	departamento_trabajo = models.ForeignKey(Departamento, db_column='DepartamentoTrabajo', verbose_name='Departamento*', blank=True, null=True, related_name='departamento_trabajo_act')
	municipio_trabajo = models.ForeignKey(Municipio, db_column='MunicipioTrabajo', verbose_name='Municipio*', blank=True, null=True, related_name='municipio_trabajo_act')
	lugar_trabajo = models.CharField(db_column='LugarTrabajo', max_length=255, blank=True, null=True, verbose_name='Lugar de Trabajo*')
	referencia_trabajo = models.CharField(db_column='ReferenciaTrabajo', max_length=1000, blank=True, null=True, verbose_name='Referencia*')
	telefono_fijo_trabajo = models.CharField(db_column='TelefonoFijoTrabajo', max_length=12, blank=True, null=True, verbose_name='Teléfono')
	correo_electronico_trabajo = models.CharField(db_column='CorreoElectronicoTrabajo', max_length=100, blank=True, null=True, verbose_name='Correo Electrónio')
	actualizado = models.BooleanField(db_column='Actualizado', default=False)
	sucursal = models.ForeignKey(Sucursal, db_column='Sucursal', max_length=255, blank=True, null=True)
	agente = models.ForeignKey(User, db_column='Agente', null=True, blank=True, related_name='agente_actualizar')
	filial =  models.ForeignKey(Filial, db_column='Filial', blank=True, null=True)
	actualizado_por = models.ForeignKey(User, db_column='ActualizadoPor', related_name='actualizado_por_actualizar')
	fecha_actualizacion = models.DateTimeField(db_column='FechaActualizacion', auto_now=True)
	codigo_rechazo = models.IntegerField(db_column='CodigoRechazo', blank=True, null=True)
	comentarios = models.CharField(db_column='Comentarios', max_length=155, blank=True, null=True)
	profesion_cliente = models.ForeignKey(Profesion, db_column='ProfesionCliente', blank=True, null=True, verbose_name='Profesión')
	actividad_cliente = models.ForeignKey(ActividadEconomica, db_column='ActividadCliente', blank=True, null=True, verbose_name='Rubro')
	con_coopcel = models.NullBooleanField(db_column='ConCoopcel', default=False)

	class Meta:
		db_table = 'ClientesActualizar'
	def __unicode__(self):
		return u'%s - %s %s %s %s' % (self.identidad, self.primer_nombre, self.segundo_apellido, self.primer_apellido, self.segundo_apellido)


class ClienteGeneral(models.Model):
	codigo = models.CharField(db_column='CodCliente', max_length=100)
	identidad = models.CharField(db_column='Identidad', max_length=20)
	primer_nombre = models.CharField(db_column='PrimerNombre', max_length=255)
	primer_apellido = models.CharField(db_column='PrimerApellido', max_length=255)
	segundo_apellido = models.CharField(db_column='SegundoApellido', max_length=255, blank=True, null=True)
	sexo = models.IntegerField(db_column='Sexo', choices=GENERO)
	estado_civil = models.IntegerField(db_column='EstadoCivil', blank=True, null=True)
	departamento = models.ForeignKey(Departamento, db_column='Departamento', blank=True, null=True, related_name='departamento_propio_gen', verbose_name='Departamento')
	municipio = models.ForeignKey(Municipio, db_column='Municipio', blank=True, null=True, related_name='municipio_propio_gen', verbose_name='Municipio')
	colonia = models.CharField(db_column='Colonia', max_length=150, blank=True, null=True, verbose_name='Dirección Completa')
	referencia = models.CharField(db_column='Referencia', max_length=1000, blank=True, null=True)
	telefono_fijo = models.CharField(db_column='TelefonoFijo', max_length=12, blank=True, null=True, verbose_name='Teléfono Fijo')
	telefono_celular = models.CharField(db_column='TelefonoCelular', max_length=12, blank=True, null=True)
	correo_electronico = models.CharField(db_column='CorreoElectronico', max_length=100, blank=True, null=True)
	profesion = models.CharField(db_column='Profesion', max_length=255, blank=True, null=True, verbose_name='Profesión u Oficio')
	ingresos = models.IntegerField(db_column='Ingresos', blank=True, null=True)
	monto_cuentas = models.FloatField(db_column='MontoCuentas', blank=True, null=True, verbose_name='Promedio de Ahorro Mensual')
	departamento_trabajo = models.ForeignKey(Departamento, db_column='DepartamentoTrabajo', verbose_name='Departamento', blank=True, null=True, related_name='departamento_trabajo_gen')
	municipio_trabajo = models.ForeignKey(Municipio, db_column='MunicipioTrabajo', verbose_name='Municipio', blank=True, null=True, related_name='municipio_trabajo_gen')
	lugar_trabajo = models.CharField(db_column='LugarTrabajo', max_length=255, blank=True, null=True, verbose_name='Lugar de Trabajo')
	referencia_trabajo = models.CharField(db_column='ReferenciaTrabajo', max_length=1000, blank=True, null=True, verbose_name='Referencia')
	telefono_fijo_trabajo = models.CharField(db_column='TelefonoFijoTrabajo', max_length=12, blank=True, null=True, verbose_name='Teléfono')
	correo_electronico_trabajo = models.CharField(db_column='CorreoElectronicoTrabajo', max_length=100, blank=True, null=True, verbose_name='Correo Electrónio')
	actualizado = models.BooleanField(db_column='Actualizado', default=False)
	sucursal = models.ForeignKey(Sucursal, db_column='Sucursal', max_length=255, blank=True, null=True)
	agente = models.ForeignKey(User, db_column='Agente', null=True, blank=True, related_name='agente_gen')
	filial =  models.ForeignKey(Filial, db_column='Filial', blank=True, null=True)
	actualizado_por = models.ForeignKey(User, db_column='ActualizadoPor', related_name='actualizado_por_gen')
	fecha_actualizacion = models.DateTimeField(db_column='FechaActualizacion', auto_now=True)
	codigo_rechazo = models.IntegerField(db_column='CodigoRechazo', blank=True, null=True)
	comentarios = models.CharField(db_column='Comentarios', max_length=155, blank=True, null=True)
	profesion_cliente = models.ForeignKey(Profesion, db_column='ProfesionCliente', blank=True, null=True, verbose_name='Profesión')
	actividad_cliente = models.ForeignKey(ActividadEconomica, db_column='ActividadCliente', blank=True, null=True, verbose_name='Rubro')
	con_coopcel = models.NullBooleanField(db_column='ConCoopcel', default=False)

	class Meta:
		db_table = 'ClientesGenerales'
	def __unicode__(self):
		return u'%s - %s %s %s %s' % (self.identidad, self.primer_nombre, self.segundo_apellido, self.primer_apellido, self.segundo_apellido)


TIPO_GESTION = {
	(1, 'Cliente Actualizado'),
	(2, 'Cliente No Localizado'),
	(3, 'Devolver Llamada Cliente'),
	(4, 'El Cliente no quiso Llenar la Informacion'),
	(5, 'Actualizado por Busqueda'),
}

class Gestion(models.Model):
	agente = models.ForeignKey(User, db_column='Agente')
	cliente_localizado = models.ForeignKey(ClienteHistorico,  db_column='ClienteLocalizado', related_name='cliente_localizado_his', blank=True, null=True)
	cliente_rechazado = models.ForeignKey(ClienteHistorico,  db_column='ClienteRechazado', related_name='cliente_rechazado_his', blank=True, null=True)
	cliente_no_localizado = models.ForeignKey(Cliente,  db_column='ClienteNoLocalizado', blank=True, null=True)
	cliente_pendiente = models.ForeignKey(ClienteActualizar,  db_column='ClientePendiente', blank=True, null=True)
	telefono = models.CharField(db_column='Telefono', max_length=12)
	fecha = models.DateField(auto_now=True,  db_column='Fecha')
	hora_incio = models.DateTimeField(db_column='HoraInicio')
	hora_final = models.DateTimeField(db_column='HoraFinal', auto_now=True)
	tipo_gestion = models.IntegerField(db_column='TipoGestion')
	identidad =  models.CharField(db_column='IdentidadCliente', max_length=15, null=True)
	cliente =  models.IntegerField(db_column='CodigoCliente', null=True)
	nombre_contacto =  models.CharField(db_column='NombreContacto',  max_length=100, null=True, blank=True)
	telefono_contacto =  models.CharField(db_column='TelefonoContacto', max_length=12,  null=True, blank=True)
	devolver_llamada =  models.CharField(db_column='DevolverLlamada', max_length=40,  null=True, blank=True)
	class Meta:
		db_table = 'Gestiones'


	def __unicode__(self):
		return u'%s - %s %s %s %s' % (self.agente.username)

