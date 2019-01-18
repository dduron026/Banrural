from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

def user_unicode_patch(self):
	return '%s %s' % (self.first_name, self.last_name)

User.__unicode__ = user_unicode_patch
def directorio_upload(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	return 'uploads/user_{0}/{1}'.format(instance.agente.id, filename.encode('ascii', 'ignore'))


class Clientes(models.Model):
	cliente = models.AutoField(db_column='CodCliente', primary_key=True)  # Field name made lowercase.
	cliente_interno = models.CharField(db_column='CodClienteInterno', max_length=20)  # Field name made lowercase.
	cliente_id = models.CharField(db_column='ClienteID', max_length=20)  # Field name made lowercase.
	nombre = models.CharField(db_column='NombreCompleto', max_length=200)  # Field name made lowercase.
	cant_creditos = models.IntegerField(db_column='CantCreditos', blank=True, null=True)  # Field name made lowercase.
	saldo_total_creditos = models.DecimalField(db_column='SaldoTotalCreditos', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
	capital_mora = models.DecimalField(db_column='CapitalMora', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
	intereses_mora = models.DecimalField(db_column='InteresesMora', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
	intereses_moratorios = models.DecimalField(db_column='InteresesMoratorios', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
	otros_recargos = models.DecimalField(db_column='OtrosRecargos', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
	dias_atraso = models.IntegerField(db_column='DiasAtraso', blank=True, null=True)  # Field name made lowercase.
	cuotas_mora = models.IntegerField(db_column='CuotasMora', blank=True, null=True)  # Field name made lowercase.
	agencia = models.IntegerField(db_column='Agencia', blank=True, null=True)  # Field name made lowercase.
	pestana = models.ForeignKey('Tipospestanas', models.DO_NOTHING, db_column='CodPestana', blank=True, null=True)  # Field name made lowercase.
	estado = models.ForeignKey('Tiposestados', models.DO_NOTHING, db_column='CodEstado', blank=True, null=True)  # Field name made lowercase.
	agente = models.ForeignKey(User, models.DO_NOTHING, db_column='CodAgente', blank=True, null=True)  # Field name made lowercase.
	sexo = models.CharField(db_column='Sexo', max_length=1, blank=True, null=True)  # Field name made lowercase.
	identidad = models.CharField(db_column='Identidad', max_length=15, blank=True, null=True)  # Field name made lowercase.
	correo_electronico = models.CharField(db_column='CorreoElectronico', max_length=50, blank=True, null=True)  # Field name made lowercase.
	hoy_actualizado = models.NullBooleanField(db_column='HoyActualizado', max_length=50, blank=True, null=True)  # Field name made lowercase.
	tiene_promesa = models.NullBooleanField(db_column='TienePromesa', max_length=50, blank=True, null=True)  # Field name made lowercase.
	proxima_fecha_pago = models.DateField(db_column='ProximaFechaPago', max_length=50, blank=True, null=True)  # Field name made lowercase.
	status = models.NullBooleanField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.
	cuenta = models.CharField(db_column='Cuenta', max_length=50)  # Field name made lowercase.
	credito = models.CharField(db_column='Credito', max_length=50)  # Field name made lowercase.
	producto_credito = models.CharField(db_column='ProductoCredito', max_length=50)  # Field name made lowercase.
	ejecutivo_id = models.IntegerField(db_column='EjecutivoID', blank=True, null=True)
	cuota = models.DecimalField(db_column='Cuota', blank=True, null=True, max_digits=10, decimal_places=2)
	fecha_actualizado_merge = models.DateTimeField(db_column='FechaActualizadoMerge', max_length=50, blank=True, null=True)


	class Meta:
		managed = False
		db_table = 'CCCOB].[Clientes'# 'CCCOB\".\"Clientes'

	def __unicode__(self):
		return self.nombre


class ClientesDirecciones(models.Model):
	codireccion = models.AutoField(db_column='CodDireccion', primary_key=True)  # Field name made lowercase.
	cliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='CodCliente')  # Field name made lowercase.
	tipo_direcciones = models.ForeignKey('Tiposdirecciones', models.DO_NOTHING, db_column='CodTipoDirecciones', blank=True, null=True)  # Field name made lowercase.
	departamento = models.ForeignKey('Departamentos', models.DO_NOTHING, db_column='CodDepartamento', blank=True, null=True)  # Field name made lowercase.
	municipio = models.ForeignKey('Municipios', models.DO_NOTHING, db_column='CodMunicipio', blank=True, null=True)  # Field name made lowercase.
	colonia = models.ForeignKey('Colonias', models.DO_NOTHING, db_column='CodColonia', blank=True, null=True)  # Field name made lowercase.
	direccion = models.CharField(db_column='Direccion', max_length=200, blank= True, null=True)  # Field name made lowercase.
	activo = models.NullBooleanField(db_column='Activo')  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'CCCOB].[ClientesXDirecciones'

	def __unicode__(self):
		return '%s|%s'%(self.cliente.nombre,self.direccion)


class ClientesGestiones(models.Model):
	gestion = models.AutoField(db_column='CodGestion', primary_key=True)  # Field name made lowercase.
	cliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='CodCliente', blank=True, null=True, related_name='cliente_gestion')  # Field name made lowercase.
	tipo_gestion = models.ForeignKey('Tiposgestion', models.DO_NOTHING, db_column='CodTipoGestion', blank=True, null=True)  # Field name made lowercase.
	resultado_gestion = models.ForeignKey('Resultadogestion', models.DO_NOTHING, db_column='CodResultadoGestion', blank=True, null=True)  # Field name made lowercase.
	telefono = models.ForeignKey('ClientesTelefono',db_column='CodTelefono', blank=True, null=True)  # Field name made lowercase.
	observaciones = models.TextField(db_column='Observaciones')  # Field name made lowercase.
	razon = models.CharField(db_column='Razon', max_length=150, blank=True, null=True)  # Field name made lowercase.
	resultado_razon = models.CharField(db_column='ResultadoRazon', max_length=150, blank=True, null=True)  # Field name made lowercase.
	fecha_inicio = models.DateTimeField(db_column='FechaInicio', blank=True, null=True)  # Field name made lowercase.
	fecha_final = models.DateTimeField(db_column='FechaFinal', blank=True, null=True, auto_now_add=True)  # Field name made lowercase.
	agente = models.ForeignKey(User, db_column='CodAgente', blank=True, null=True)  # Field name made lowercase.
	devolver_llamada = models.DateTimeField(db_column='DevolverLlamada', blank=True, null=True)  # Field name made lowercase.
	nombre_contacto = models.CharField(db_column='NombreContacto', max_length=150, blank=True, null=True)  # Field name made lowercase.
	telefono_contacto = models.CharField(db_column='TelefonoContacto', max_length=150, blank=True, null=True)  # Field name made lowercase.
	nombre_gestor = models.CharField(db_column='name_gestor', max_length=150, blank=True, null=True)  # Field name made lowercase.
	adjunto  = models.FileField(db_column='Adjunto', upload_to=directorio_upload, blank=True, null=True)
	bufete = models.IntegerField(db_column='Bufete', blank=True, null=True)  # Field name made lowercase.
	direccion = models.IntegerField(db_column='CodDireccion', blank=True, null=True)  # Field name made lowercase.
	nombre_tercero = models.CharField(db_column='NombreTercero', max_length=150, blank=True, null=True)  # Field name made lowercase.
	correo = models.CharField(db_column='CorreoElectronico', max_length=50, blank=True, null=True)  # Field name made lowercase.
	titulo_mensaje = models.CharField(db_column='TituloMensaje', max_length=50, blank=True, null=True)  # Field name made lowercase.
	mensaje = models.TextField(db_column='Mensaje', blank=True, null=True)  # Field name made lowercase.
	cliente_interno = models.CharField(db_column='CodClienteInterno', blank=True, null=True, max_length=50)  # Field name made lowercase.
	fecha_gestion = models.DateField(db_column='FechaGestion',null=True,blank=True)
	monto_promesa = models.IntegerField(db_column='MontoPromesa', null=True,blank=True)

	class Meta:
		managed = False
		db_table = 'CCCOB].[ClientesXGestiones'

	def __unicode__(self):
		return '%s|%s'%(self.cliente.nombre, self.tipo_gestion.descripcion)


class ClientesPromesas(models.Model):
	promesa = models.AutoField(db_column='CodPromesa', primary_key=True)  # Field name made lowercase.
	cliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='CodCliente', blank=True, null=True, related_name='cliente_promesas')  # Field name made lowercase.
	fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
	agente = models.ForeignKey(User, db_column='CodAgente', blank=True, null=True, related_name='cliente_agente')  # Field name made lowercase.
	fecha_gestion = models.DateTimeField(db_column='FechaGestion', auto_now_add=True)  # Field name made lowercase.	
	estado = models.CharField(db_column='Estado', max_length=150, blank=True, null=True)  # Field name made lowercase.
	nombre_agente = models.CharField(db_column='NombreAgente', max_length=150, blank=True, null=True)  # Field name made lowercase.
	monto_promesa = models.IntegerField(db_column='MontoPromesa', null=True,blank=True)
	cod_gestion = models.ForeignKey(ClientesGestiones, models.DO_NOTHING, db_column='CodGestion',blank=True,null=True, related_name='cliente_gestion')
	cliente_interno = models.CharField(db_column='CodClienteInterno', blank=True, null=True, max_length=50)
	cuota = models.DecimalField(db_column='Cuota', blank=True, null=True, max_digits=10, decimal_places=2)

	class Meta:
		managed = False
		db_table = 'CCCOB].[ClientesXPromesaPago'

	def __unicode__(self):
		return '%s|%s'%(self.cliente.nombre, self.fecha)


class Agentes(models.Model):
	agente = models.AutoField(db_column='CodAgente', primary_key=True)  # Field name made lowercase.
	usuario = models.ForeignKey(User, models.DO_NOTHING, db_column='CodUsuario', related_name='usuario_agente')  # Field name made lowercase.
	telefono = models.CharField(db_column='Telefono', max_length=20)  # Field name made lowercase.
	cargo = models.CharField(db_column='Cargo', max_length=20)  # Field name made lowercase.
	nombre = models.CharField(db_column = 'Nombre', max_length=100)
	correo = models.CharField(db_column = 'Correo', max_length=100)
	# persona_referida = models.CharField(db_column='PersonaReferida')

	class Meta:
		managed = False
		db_table = 'CCCOB].[Agentes'

	def __unicode__(self):
		return '%s'%(self.usuario.username)

class ClientesTelefono(models.Model):
	cod_telefono = models.AutoField(db_column='CodTelefono', primary_key=True)  # Field name made lowercase.
	cliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='CodCliente', related_name='cliente_telefono')  # Field name made lowercase.
	tipo_telefono = models.ForeignKey('Tipostelefonos', models.DO_NOTHING, db_column='CodTipoTelefono', blank=True, null=True)  # Field name made lowercase.
	telefono = models.CharField(db_column='Telefono', max_length=20)  # Field name made lowercase.
	mensaje = models.NullBooleanField(db_column='Mensaje')  # Field name made lowercase.
	activo = models.NullBooleanField(db_column='Activo')  # Field name made lowercase.
	persona_referida = models.CharField(db_column = 'PersonaReferida', max_length=100)
	# persona_referida = models.CharField(db_column='PersonaReferida')

	class Meta:
		managed = False
		db_table = 'CCCOB].[ClientesXTelefono'

	def __unicode__(self):
		return '%s|%s'%(self.cliente.nombre, self.telefono)


class Colonias(models.Model):
	colonia = models.AutoField(db_column='CodColonia', primary_key=True)  # Field name made lowercase.
	municipio = models.ForeignKey('Municipios', models.DO_NOTHING, db_column='CodMunicipio', blank=True, null=True)  # Field name made lowercase.
	descripcion = models.CharField(db_column='DescColonia', max_length=200)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'CCCOB].[Colonias'

	def __unicode__(self):
		return self.descripcion


class Departamentos(models.Model):
	descripcion = models.CharField(db_column='DescDepartamento', max_length=100)  # Field name made lowercase.
	codigo = models.AutoField(db_column='CodDepartamento', primary_key=True)  # Field name made lowercase.


	class Meta:
		managed = False
		db_table = 'CCCOB].[Departamentos'

	def __unicode__(self):
		return self.descripcion

class GlobalParameters(models.Model):
	nombre_empresa = models.CharField(db_column='NombreEmpresa', max_length=150, blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'CCCOB].[GlobalParameters'

	def __unicode__(self):
		return self.nombre_empresa


class Municipios(models.Model):
	municipio = models.AutoField(db_column='CodMunicipio', primary_key=True)  # Field name made lowercase.
	departamento = models.ForeignKey(Departamentos, models.DO_NOTHING, db_column='CodDepartamento', blank=True, null=True)  # Field name made lowercase.
	descripcion = models.CharField(db_column='DescMunicipio', max_length=200)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'CCCOB].[Municipios'

	def __unicode__(self):
		return self.descripcion


class ResultadoGestion(models.Model):
	resultado_gestion = models.AutoField(db_column='CodResultadoGestion', primary_key=True)  # Field name made lowercase.
	descripcion = models.CharField(db_column='DescResultadoGestion', max_length=200)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'CCCOB].[ResultadoGestion'

	def __unicode__(self):
		return self.descripcion


class TiposDirecciones(models.Model):
	tipo_direcciones = models.AutoField(db_column='CodTipoDirecciones', primary_key=True)  # Field name made lowercase.
	descripcion = models.CharField(db_column='DescTipoTDirecciones', max_length=30, blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'CCCOB].[TiposDirecciones'

	def __unicode__(self):
		return self.descripcion



class TiposEstados(models.Model):
	estado = models.AutoField(db_column='CodEstado', primary_key=True)  # Field name made lowercase.
	descripcion = models.CharField(db_column='DescEstado', max_length=30, blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'CCCOB].[TiposEstados'

	def __unicode__(self):
		return self.descripcion


class TiposGestion(models.Model):
	tipo_gestion = models.AutoField(db_column='CodTipoGestion', primary_key=True)  # Field name made lowercase.
	descripcion = models.CharField(db_column='DescTipoGestion', max_length=200)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'CCCOB].[TiposGestion'

	def __unicode__(self):
		return self.descripcion


class TiposPestanas(models.Model):
	pestana = models.AutoField(db_column='CodPestana', primary_key=True)  # Field name made lowercase.
	descripcion = models.CharField(db_column='DescPestana', max_length=30, blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'CCCOB].[TiposPestanas'

	def __unicode__(self):
		return self.descripcion


class TiposTelefonos(models.Model):
	tipotelefono = models.AutoField(db_column='CodTipoTelefono', primary_key=True)  # Field name made lowercase.
	descripcion = models.CharField(db_column='DescTipoTelefono', max_length=30, blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'CCCOB].[TiposTelefonos'

	def __unicode__(self):
		return self.descripcion

class Agencias(models.Model):
	codigo_agencia = models.AutoField(db_column='CodigoAgencia', primary_key=True)  # Field name made lowercase.
	codigo_agenciabw = models.CharField(db_column='CodigoAgenciaBW', max_length=5, blank=True, null=True)  # Field name made lowercase.
	centro_costo = models.CharField(db_column='CentrodeCosto', max_length=5, blank=True, null=True)  # Field name made lowercase.
	nombre_agencia = models.CharField(db_column='NombreAgencia', max_length=100, blank=True, null=True)  # Field name made lowercase.
	departamento = models.CharField(db_column='Departamento', max_length=100, blank=True, null=True)  # Field name made lowercase.
	municipio = models.CharField(db_column='Municipio', max_length=100, blank=True, null=True)  # Field name made lowercase.
	ciudad = models.CharField(db_column='Ciudad', max_length=100, blank=True, null=True)  # Field name made lowercase.
	activo = models.NullBooleanField(db_column='Activo')  # Field name made lowercase.
	fecha_creacion = models.DateTimeField(db_column='FechaCreacion', blank=True, null=True)  # Field name made lowercase.
	telefono = models.CharField(db_column='Telefono', max_length=20, blank=True, null=True)  # Field name made lowercase.
	direccion = models.CharField(db_column='Direccion', max_length=150, blank=True, null=True)  # Field name made lowercase.
	mapa_departamento = models.DecimalField(db_column='CodigoMapaDepartamento', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
	region = models.CharField(db_column='Region', max_length=50, blank=True, null=True)  # Field name made lowercase.
	codigo_region = models.IntegerField(db_column='CodigoRegion', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'CCCOB].[Agencias'

	def __unicode__(self):
		return self.nombre_agencia

class Bufetes(models.Model):
	bufete = models.AutoField(db_column='CodBufete', primary_key=True)  # Field name made lowercase.
	descripcion = models.CharField(db_column='DescBufete', max_length=200)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'CCCOB].[Bufetes'

	def __unicode__(self):
		return self.descripcion


class ProductosCredito(models.Model):
	producto = models.AutoField(db_column='CodProducto', primary_key=True)  # Field name made lowercase.
	nombre_corto = models.CharField(db_column='NombreCorto', max_length=200)  # Field name made lowercase.
	nombre_largo = models.CharField(db_column='NombreLargo', max_length=200)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'CCCOB].[ProductosCredito'

	def __unicode__(self):
		return '%s | %s'%(self.producto, self.nombre_corto)


class HistorialAsignacion(models.Model):
	cod_historial = models.AutoField(db_column='CodHistorial', primary_key=True)  # Field name made lowercase.
	productos = models.TextField(db_column='Productos')  # Field name made lowercase.
	agencias = models.TextField(db_column='Agencias')  # Field name made lowercase.
	dias_mora = models.CharField(db_column='DiasMora', max_length=200)  # Field name made lowercase.
	capital_mora = models.CharField(db_column='CapitalMora', max_length=200)  # Field name made lowercase.
	agente = models.ForeignKey(User, db_column='Agente', related_name="agente_historial")  # Field name made lowercase.
	fecha = models.DateTimeField(db_column='Fecha', auto_now_add=True)  # Field name made lowercase.
	estado = models.NullBooleanField(db_column='Estado', max_length=200)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'CCCOB].[HistorialAsignacion'

	def __unicode__(self):
		return '%s | %s'%(self.agente, self.fecha)