# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class 03CarteraMoraDelDia(models.Model):
    region = models.CharField(db_column='Region', max_length=255, blank=True, null=True)  # Field name made lowercase.
    agencia = models.CharField(db_column='Agencia', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nocredito = models.CharField(db_column='NoCredito', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codcliente = models.CharField(db_column='CodCliente', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nombre_cliente = models.CharField(db_column='Nombre Cliente', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    identificacion = models.CharField(db_column='Identificacion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    direcci_n = models.TextField(db_column='Direcci\xf3n', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tel_fono = models.CharField(db_column='Tel\xe9fono', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    codeudor = models.CharField(db_column='Codeudor', max_length=255, blank=True, null=True)  # Field name made lowercase.
    aval1 = models.CharField(db_column='Aval1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    aval2 = models.CharField(db_column='Aval2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fecha_desembolso = models.DateTimeField(db_column='Fecha Desembolso', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fecha_cierre = models.DateTimeField(db_column='Fecha Cierre', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    moneda = models.CharField(db_column='Moneda', max_length=255, blank=True, null=True)  # Field name made lowercase.
    saldo_inicial_hnl = models.FloatField(db_column='Saldo Inicial HNL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    saldo_inicial_usd = models.FloatField(db_column='Saldo Inicial  USD', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tasa_desembolso = models.FloatField(db_column='Tasa Desembolso', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    saldo_hnl = models.FloatField(db_column='Saldo HNL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    saldo_usd = models.FloatField(db_column='Saldo USD', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tasa_actual = models.FloatField(db_column='Tasa Actual', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    interes_hnl = models.FloatField(db_column='Interes HNL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tasa_cr_dito = models.FloatField(db_column='Tasa Cr\xe9dito', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dias_mora = models.FloatField(db_column='Dias Mora', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    forma_pago = models.CharField(db_column='Forma Pago', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fecha_proximo_pago = models.DateTimeField(db_column='Fecha Proximo Pago', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_cuota_proyectada = models.FloatField(db_column='Total Cuota Proyectada', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cuota_mora = models.FloatField(db_column='Cuota Mora', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    capital_mora = models.FloatField(db_column='Capital Mora', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    interes_mora = models.FloatField(db_column='Interes Mora', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    recargos = models.FloatField(db_column='Recargos', blank=True, null=True)  # Field name made lowercase.
    gestion_mora = models.FloatField(db_column='Gestion Mora', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    interes_vencido = models.FloatField(db_column='Interes Vencido', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    interes_refinanciado = models.FloatField(db_column='Interes Refinanciado', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cargos_adicionales = models.FloatField(db_column='Cargos Adicionales', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    saldo_mora = models.FloatField(db_column='Saldo Mora', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_deuda = models.FloatField(db_column='Total Deuda', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cuenta_corriente_ahorro = models.CharField(db_column='Cuenta Corriente/Ahorro', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    saldo_cuenta = models.FloatField(db_column='Saldo Cuenta', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    analista = models.CharField(db_column='Analista', max_length=255, blank=True, null=True)  # Field name made lowercase.
    refinanciado = models.FloatField(db_column='Refinanciado', blank=True, null=True)  # Field name made lowercase.
    garantia = models.CharField(db_column='Garantia', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fondos = models.CharField(db_column='Fondos', max_length=255, blank=True, null=True)  # Field name made lowercase.
    linea = models.CharField(db_column='Linea', max_length=255, blank=True, null=True)  # Field name made lowercase.
    oper = models.FloatField(db_column='Oper')  # Field name made lowercase.
    cif = models.FloatField(db_column='CIF', blank=True, null=True)  # Field name made lowercase.
    rango_mora = models.CharField(db_column='Rango Mora', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fechar = models.DateTimeField(db_column='FechaR', blank=True, null=True)  # Field name made lowercase.
    tipomora = models.CharField(db_column='TipoMora', max_length=255, blank=True, null=True)  # Field name made lowercase.
    division_mora = models.CharField(db_column='Division Mora', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    factor_d = models.FloatField(db_column='Factor_D', blank=True, null=True)  # Field name made lowercase.
    cant = models.FloatField(db_column='Cant', blank=True, null=True)  # Field name made lowercase.
    diasmoracliente = models.IntegerField(db_column='DiasMoraCliente', blank=True, null=True)  # Field name made lowercase.
    proyecto_financiamiento = models.CharField(db_column='Proyecto_Financiamiento', max_length=255, blank=True, null=True)  # Field name made lowercase.
    oldnumber = models.FloatField(db_column='OldNumber', blank=True, null=True)  # Field name made lowercase.
    gestor = models.IntegerField(db_column='Gestor', blank=True, null=True)  # Field name made lowercase.
    codanalista = models.IntegerField(db_column='CodAnalista', blank=True, null=True)  # Field name made lowercase.
    tipo_credito = models.CharField(db_column='Tipo_Credito', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '03 Cartera Mora del Dia'


class 99AsignacionPremoraCallCenter(models.Model):
    region = models.CharField(db_column='Region', max_length=255, blank=True, null=True)  # Field name made lowercase.
    agencia = models.CharField(db_column='Agencia', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nocredito = models.CharField(db_column='NoCredito', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codcliente = models.CharField(db_column='CodCliente', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nombre_cliente = models.CharField(db_column='Nombre Cliente', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    moneda = models.CharField(db_column='Moneda', max_length=255, blank=True, null=True)  # Field name made lowercase.
    saldo_hnl = models.FloatField(db_column='Saldo HNL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    interes_hnl = models.FloatField(db_column='Interes HNL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dias_mora = models.FloatField(db_column='Dias Mora', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fecha_proximo_pago = models.CharField(db_column='Fecha Proximo Pago', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_deuda = models.FloatField(db_column='Total Deuda', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    linea = models.CharField(db_column='Linea', max_length=255, blank=True, null=True)  # Field name made lowercase.
    garantia = models.CharField(db_column='Garantia', max_length=255, blank=True, null=True)  # Field name made lowercase.
    oper = models.FloatField(db_column='Oper', blank=True, null=True)  # Field name made lowercase.
    tipomora = models.CharField(db_column='TipoMora', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gestor = models.IntegerField(db_column='Gestor', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '99 Asignacion Premora Call Center'


class ActividadesEconomicas(models.Model):
    codigo_actividad_economica = models.AutoField(db_column='CODIGO_ACTIVIDAD_ECONOMICA', primary_key=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='DESCRIPCION', max_length=60, blank=True, null=True)  # Field name made lowercase.
    activo_b = models.CharField(db_column='ACTIVO_B', max_length=1, blank=True, null=True)  # Field name made lowercase.
    creado_por = models.CharField(db_column='CREADO_POR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fecha_creacion = models.CharField(db_column='FECHA_CREACION', max_length=27, blank=True, null=True)  # Field name made lowercase.
    modificado_por = models.CharField(db_column='MODIFICADO_POR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fecha_modificacion = models.CharField(db_column='FECHA_MODIFICACION', max_length=27, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ACTIVIDADES_ECONOMICAS'


class Acciones(models.Model):
    codaccion = models.IntegerField(db_column='CodAccion', primary_key=True)  # Field name made lowercase.
    codreclamo = models.ForeignKey('Reclamos', models.DO_NOTHING, db_column='CodReclamo', blank=True, null=True)  # Field name made lowercase.
    ordennominal = models.IntegerField(db_column='OrdenNominal', blank=True, null=True)  # Field name made lowercase.
    fechahora = models.DateTimeField(db_column='FechaHora', blank=True, null=True)  # Field name made lowercase.
    oficialaccion = models.IntegerField(db_column='OficialAccion', blank=True, null=True)  # Field name made lowercase.
    codtipoacciones = models.ForeignKey('Tipoacciones', models.DO_NOTHING, db_column='CodTipoAcciones', blank=True, null=True)  # Field name made lowercase.
    observaciones = models.CharField(db_column='Observaciones', max_length=500, blank=True, null=True)  # Field name made lowercase.
    adjunto = models.CharField(db_column='Adjunto', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Acciones'


class Agencias(models.Model):
    codigoagencia = models.IntegerField(db_column='CodigoAgencia', primary_key=True)  # Field name made lowercase.
    codigoagenciabw = models.CharField(db_column='CodigoAgenciaBW', max_length=5, blank=True, null=True)  # Field name made lowercase.
    centrodecosto = models.CharField(db_column='CentrodeCosto', max_length=5, blank=True, null=True)  # Field name made lowercase.
    nombreagencia = models.CharField(db_column='NombreAgencia', max_length=100, blank=True, null=True)  # Field name made lowercase.
    departamento = models.CharField(db_column='Departamento', max_length=100, blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='Municipio', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ciudad = models.CharField(db_column='Ciudad', max_length=100, blank=True, null=True)  # Field name made lowercase.
    activo = models.NullBooleanField(db_column='Activo')  # Field name made lowercase.
    fechacreacion = models.DateTimeField(db_column='FechaCreacion', blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=20, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=150, blank=True, null=True)  # Field name made lowercase.
    codigomapadepartamento = models.DecimalField(db_column='CodigoMapaDepartamento', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    region = models.CharField(db_column='Region', max_length=50, blank=True, null=True)  # Field name made lowercase.
    codigoregion = models.IntegerField(db_column='CodigoRegion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Agencias'


class Agentes(models.Model):
    codagente = models.IntegerField(db_column='CodAgente', primary_key=True)  # Field name made lowercase.
    codusuario = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='CodUsuario', blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=20, blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=200)  # Field name made lowercase.
    cargo = models.CharField(db_column='Cargo', max_length=200, blank=True, null=True)  # Field name made lowercase.
    correo = models.CharField(db_column='Correo', max_length=200, blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='Municipio', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Agentes'


class Bufetes(models.Model):
    codbufete = models.IntegerField(db_column='CodBufete', primary_key=True)  # Field name made lowercase.
    descbufete = models.CharField(db_column='DescBufete', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Bufetes'


class Categorias(models.Model):
    codcategoria = models.IntegerField(db_column='CodCategoria', primary_key=True)  # Field name made lowercase.
    desccategoria = models.CharField(db_column='DescCategoria', max_length=75, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Categorias'


class Cliente(models.Model):
    identidad = models.CharField(db_column='Identidad', max_length=20)  # Field name made lowercase.
    primernombre = models.CharField(db_column='PrimerNombre', max_length=255)  # Field name made lowercase.
    primerapellido = models.CharField(db_column='PrimerApellido', max_length=255)  # Field name made lowercase.
    segundoapellido = models.CharField(db_column='SegundoApellido', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sexo = models.IntegerField(db_column='Sexo')  # Field name made lowercase.
    estadocivil = models.IntegerField(db_column='EstadoCivil', blank=True, null=True)  # Field name made lowercase.
    colonia = models.CharField(db_column='Colonia', max_length=150, blank=True, null=True)  # Field name made lowercase.
    referencia = models.CharField(db_column='Referencia', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    telefonofijo = models.CharField(db_column='TelefonoFijo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    telefonocelular = models.CharField(db_column='TelefonoCelular', max_length=12, blank=True, null=True)  # Field name made lowercase.
    correoelectronico = models.CharField(db_column='CorreoElectronico', max_length=100, blank=True, null=True)  # Field name made lowercase.
    profesion = models.CharField(db_column='Profesion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ingresos = models.FloatField(db_column='Ingresos', blank=True, null=True)  # Field name made lowercase.
    montocuentas = models.FloatField(db_column='MontoCuentas', blank=True, null=True)  # Field name made lowercase.
    departamentotrabajo = models.ForeignKey('Departamento', models.DO_NOTHING, db_column='DepartamentoTrabajo', blank=True, null=True)  # Field name made lowercase.
    municipiotrabajo = models.ForeignKey('Municipio', models.DO_NOTHING, db_column='MunicipioTrabajo', blank=True, null=True)  # Field name made lowercase.
    lugartrabajo = models.CharField(db_column='LugarTrabajo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    referenciatrabajo = models.CharField(db_column='ReferenciaTrabajo', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    telefonofijotrabajo = models.CharField(db_column='TelefonoFijoTrabajo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    correoelectronicotrabajo = models.CharField(db_column='CorreoElectronicoTrabajo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    actualizado = models.BooleanField(db_column='Actualizado')  # Field name made lowercase.
    fechaactualizacion = models.DateTimeField(db_column='FechaActualizacion')  # Field name made lowercase.
    actualizadopor = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='ActualizadoPor')  # Field name made lowercase.
    agente = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='Agente', blank=True, null=True)  # Field name made lowercase.
    departamento = models.ForeignKey('Departamento', models.DO_NOTHING, db_column='Departamento', blank=True, null=True)  # Field name made lowercase.
    filial = models.ForeignKey('Filial', models.DO_NOTHING, db_column='Filial', blank=True, null=True)  # Field name made lowercase.
    municipio = models.ForeignKey('Municipio', models.DO_NOTHING, db_column='Municipio', blank=True, null=True)  # Field name made lowercase.
    sucursal = models.ForeignKey('Sucursal', models.DO_NOTHING, db_column='Sucursal', blank=True, null=True)  # Field name made lowercase.
    codigorechazo = models.IntegerField(db_column='CodigoRechazo', blank=True, null=True)  # Field name made lowercase.
    comentarios = models.CharField(db_column='Comentarios', max_length=155, blank=True, null=True)  # Field name made lowercase.
    codcliente = models.CharField(db_column='CodCliente', max_length=100)  # Field name made lowercase.
    actividadcliente = models.ForeignKey(ActividadesEconomicas, models.DO_NOTHING, db_column='ActividadCliente', blank=True, null=True)  # Field name made lowercase.
    profesioncliente = models.ForeignKey('Profesiones', models.DO_NOTHING, db_column='ProfesionCliente', blank=True, null=True)  # Field name made lowercase.
    concoopcel = models.NullBooleanField(db_column='ConCoopcel')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cliente'


class Clientes(models.Model):
    codcliente = models.IntegerField(db_column='CodCliente', primary_key=True)  # Field name made lowercase.
    codclienteinterno = models.CharField(db_column='CodClienteInterno', max_length=40, blank=True, null=True)  # Field name made lowercase.
    nombrecompleto = models.CharField(db_column='NombreCompleto', max_length=200)  # Field name made lowercase.
    cantcreditos = models.IntegerField(db_column='CantCreditos', blank=True, null=True)  # Field name made lowercase.
    saldototalcreditos = models.DecimalField(db_column='SaldoTotalCreditos', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    capitalmora = models.DecimalField(db_column='CapitalMora', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    interesesmora = models.DecimalField(db_column='InteresesMora', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    interesesmoratorios = models.DecimalField(db_column='InteresesMoratorios', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    otrosrecargos = models.DecimalField(db_column='OtrosRecargos', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    diasatraso = models.IntegerField(db_column='DiasAtraso', blank=True, null=True)  # Field name made lowercase.
    cuotasmora = models.IntegerField(db_column='CuotasMora', blank=True, null=True)  # Field name made lowercase.
    agencia = models.IntegerField(db_column='Agencia', blank=True, null=True)  # Field name made lowercase.
    codpestana = models.ForeignKey('Tipospestanas', models.DO_NOTHING, db_column='CodPestana', blank=True, null=True)  # Field name made lowercase.
    codestado = models.ForeignKey('Tiposestados', models.DO_NOTHING, db_column='CodEstado', blank=True, null=True)  # Field name made lowercase.
    codagente = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='CodAgente', blank=True, null=True)  # Field name made lowercase.
    correoelectronico = models.CharField(db_column='CorreoElectronico', max_length=100, blank=True, null=True)  # Field name made lowercase.
    identidad = models.CharField(db_column='Identidad', max_length=15, blank=True, null=True)  # Field name made lowercase.
    sexo = models.CharField(db_column='Sexo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    clienteid = models.CharField(db_column='ClienteID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    hoyactualizado = models.SmallIntegerField(db_column='HoyActualizado', blank=True, null=True)  # Field name made lowercase.
    tienepromesa = models.SmallIntegerField(db_column='TienePromesa', blank=True, null=True)  # Field name made lowercase.
    proximafechapago = models.CharField(db_column='ProximaFechaPago', max_length=10, blank=True, null=True)  # Field name made lowercase.
    estado = models.SmallIntegerField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.
    fechamerge = models.DateTimeField(db_column='FechaMerge', blank=True, null=True)  # Field name made lowercase.
    cuenta = models.CharField(db_column='Cuenta', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechaactualizadomerge = models.DateTimeField(db_column='FechaActualizadoMerge', blank=True, null=True)  # Field name made lowercase.
    credito = models.CharField(db_column='Credito', max_length=50, blank=True, null=True)  # Field name made lowercase.
    productocredito = models.CharField(db_column='ProductoCredito', max_length=250, blank=True, null=True)  # Field name made lowercase.
    autoasignado = models.SmallIntegerField(db_column='AutoAsignado', blank=True, null=True)  # Field name made lowercase.
    ejecutivoid = models.IntegerField(db_column='EjecutivoID', blank=True, null=True)  # Field name made lowercase.
    cuota = models.DecimalField(db_column='Cuota', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Clientes'


class Clientesactualizar(models.Model):
    identidad = models.CharField(db_column='Identidad', max_length=20)  # Field name made lowercase.
    primernombre = models.CharField(db_column='PrimerNombre', max_length=255)  # Field name made lowercase.
    primerapellido = models.CharField(db_column='PrimerApellido', max_length=255)  # Field name made lowercase.
    segundoapellido = models.CharField(db_column='SegundoApellido', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sexo = models.IntegerField(db_column='Sexo')  # Field name made lowercase.
    estadocivil = models.IntegerField(db_column='EstadoCivil', blank=True, null=True)  # Field name made lowercase.
    colonia = models.CharField(db_column='Colonia', max_length=150, blank=True, null=True)  # Field name made lowercase.
    referencia = models.CharField(db_column='Referencia', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    telefonofijo = models.CharField(db_column='TelefonoFijo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    telefonocelular = models.CharField(db_column='TelefonoCelular', max_length=12, blank=True, null=True)  # Field name made lowercase.
    correoelectronico = models.CharField(db_column='CorreoElectronico', max_length=100, blank=True, null=True)  # Field name made lowercase.
    profesion = models.CharField(db_column='Profesion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ingresos = models.IntegerField(db_column='Ingresos', blank=True, null=True)  # Field name made lowercase.
    montocuentas = models.FloatField(db_column='MontoCuentas', blank=True, null=True)  # Field name made lowercase.
    departamentotrabajo = models.ForeignKey('Departamento', models.DO_NOTHING, db_column='DepartamentoTrabajo', blank=True, null=True)  # Field name made lowercase.
    municipiotrabajo = models.ForeignKey('Municipio', models.DO_NOTHING, db_column='MunicipioTrabajo', blank=True, null=True)  # Field name made lowercase.
    lugartrabajo = models.CharField(db_column='LugarTrabajo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    referenciatrabajo = models.CharField(db_column='ReferenciaTrabajo', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    telefonofijotrabajo = models.CharField(db_column='TelefonoFijoTrabajo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    correoelectronicotrabajo = models.CharField(db_column='CorreoElectronicoTrabajo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    actualizado = models.BooleanField(db_column='Actualizado')  # Field name made lowercase.
    fechaactualizacion = models.DateTimeField(db_column='FechaActualizacion')  # Field name made lowercase.
    actualizadopor = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='ActualizadoPor')  # Field name made lowercase.
    agente = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='Agente', blank=True, null=True)  # Field name made lowercase.
    departamento = models.ForeignKey('Departamento', models.DO_NOTHING, db_column='Departamento', blank=True, null=True)  # Field name made lowercase.
    filial = models.ForeignKey('Filial', models.DO_NOTHING, db_column='Filial', blank=True, null=True)  # Field name made lowercase.
    municipio = models.ForeignKey('Municipio', models.DO_NOTHING, db_column='Municipio', blank=True, null=True)  # Field name made lowercase.
    sucursal = models.ForeignKey('Sucursal', models.DO_NOTHING, db_column='Sucursal', blank=True, null=True)  # Field name made lowercase.
    codigorechazo = models.IntegerField(db_column='CodigoRechazo', blank=True, null=True)  # Field name made lowercase.
    comentarios = models.CharField(db_column='Comentarios', max_length=155, blank=True, null=True)  # Field name made lowercase.
    codcliente = models.CharField(db_column='CodCliente', max_length=100)  # Field name made lowercase.
    actividadcliente = models.ForeignKey(ActividadesEconomicas, models.DO_NOTHING, db_column='ActividadCliente', blank=True, null=True)  # Field name made lowercase.
    profesioncliente = models.ForeignKey('Profesiones', models.DO_NOTHING, db_column='ProfesionCliente', blank=True, null=True)  # Field name made lowercase.
    concoopcel = models.NullBooleanField(db_column='ConCoopcel')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ClientesActualizar'


class Clientesgenerales(models.Model):
    codcliente = models.CharField(db_column='CodCliente', max_length=100)  # Field name made lowercase.
    identidad = models.CharField(db_column='Identidad', max_length=20)  # Field name made lowercase.
    primernombre = models.CharField(db_column='PrimerNombre', max_length=255)  # Field name made lowercase.
    primerapellido = models.CharField(db_column='PrimerApellido', max_length=255)  # Field name made lowercase.
    segundoapellido = models.CharField(db_column='SegundoApellido', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sexo = models.IntegerField(db_column='Sexo')  # Field name made lowercase.
    estadocivil = models.IntegerField(db_column='EstadoCivil', blank=True, null=True)  # Field name made lowercase.
    colonia = models.CharField(db_column='Colonia', max_length=150, blank=True, null=True)  # Field name made lowercase.
    referencia = models.CharField(db_column='Referencia', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    telefonofijo = models.CharField(db_column='TelefonoFijo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    telefonocelular = models.CharField(db_column='TelefonoCelular', max_length=12, blank=True, null=True)  # Field name made lowercase.
    correoelectronico = models.CharField(db_column='CorreoElectronico', max_length=100, blank=True, null=True)  # Field name made lowercase.
    profesion = models.CharField(db_column='Profesion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ingresos = models.IntegerField(db_column='Ingresos', blank=True, null=True)  # Field name made lowercase.
    montocuentas = models.FloatField(db_column='MontoCuentas', blank=True, null=True)  # Field name made lowercase.
    lugartrabajo = models.CharField(db_column='LugarTrabajo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    referenciatrabajo = models.CharField(db_column='ReferenciaTrabajo', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    telefonofijotrabajo = models.CharField(db_column='TelefonoFijoTrabajo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    correoelectronicotrabajo = models.CharField(db_column='CorreoElectronicoTrabajo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    actualizado = models.BooleanField(db_column='Actualizado')  # Field name made lowercase.
    fechaactualizacion = models.DateTimeField(db_column='FechaActualizacion')  # Field name made lowercase.
    codigorechazo = models.IntegerField(db_column='CodigoRechazo', blank=True, null=True)  # Field name made lowercase.
    comentarios = models.CharField(db_column='Comentarios', max_length=155, blank=True, null=True)  # Field name made lowercase.
    actividadcliente = models.ForeignKey(ActividadesEconomicas, models.DO_NOTHING, db_column='ActividadCliente', blank=True, null=True)  # Field name made lowercase.
    actualizadopor = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='ActualizadoPor')  # Field name made lowercase.
    agente = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='Agente', blank=True, null=True)  # Field name made lowercase.
    departamento = models.ForeignKey('Departamento', models.DO_NOTHING, db_column='Departamento', blank=True, null=True)  # Field name made lowercase.
    departamentotrabajo = models.ForeignKey('Departamento', models.DO_NOTHING, db_column='DepartamentoTrabajo', blank=True, null=True)  # Field name made lowercase.
    filial = models.ForeignKey('Filial', models.DO_NOTHING, db_column='Filial', blank=True, null=True)  # Field name made lowercase.
    municipio = models.ForeignKey('Municipio', models.DO_NOTHING, db_column='Municipio', blank=True, null=True)  # Field name made lowercase.
    municipiotrabajo = models.ForeignKey('Municipio', models.DO_NOTHING, db_column='MunicipioTrabajo', blank=True, null=True)  # Field name made lowercase.
    profesioncliente = models.ForeignKey('Profesiones', models.DO_NOTHING, db_column='ProfesionCliente', blank=True, null=True)  # Field name made lowercase.
    sucursal = models.ForeignKey('Sucursal', models.DO_NOTHING, db_column='Sucursal', blank=True, null=True)  # Field name made lowercase.
    concoopcel = models.NullBooleanField(db_column='ConCoopcel')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ClientesGenerales'


class Clienteshistoricos(models.Model):
    identidad = models.CharField(db_column='Identidad', max_length=20)  # Field name made lowercase.
    primernombre = models.CharField(db_column='PrimerNombre', max_length=255)  # Field name made lowercase.
    primerapellido = models.CharField(db_column='PrimerApellido', max_length=255)  # Field name made lowercase.
    segundoapellido = models.CharField(db_column='SegundoApellido', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sexo = models.IntegerField(db_column='Sexo')  # Field name made lowercase.
    estadocivil = models.IntegerField(db_column='EstadoCivil', blank=True, null=True)  # Field name made lowercase.
    colonia = models.CharField(db_column='Colonia', max_length=150, blank=True, null=True)  # Field name made lowercase.
    referencia = models.CharField(db_column='Referencia', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    telefonofijo = models.CharField(db_column='TelefonoFijo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    telefonocelular = models.CharField(db_column='TelefonoCelular', max_length=12, blank=True, null=True)  # Field name made lowercase.
    correoelectronico = models.CharField(db_column='CorreoElectronico', max_length=100, blank=True, null=True)  # Field name made lowercase.
    profesion = models.CharField(db_column='Profesion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ingresos = models.FloatField(db_column='Ingresos', blank=True, null=True)  # Field name made lowercase.
    montocuentas = models.FloatField(db_column='MontoCuentas', blank=True, null=True)  # Field name made lowercase.
    departamentotrabajo = models.ForeignKey('Departamento', models.DO_NOTHING, db_column='DepartamentoTrabajo', blank=True, null=True)  # Field name made lowercase.
    municipiotrabajo = models.ForeignKey('Municipio', models.DO_NOTHING, db_column='MunicipioTrabajo', blank=True, null=True)  # Field name made lowercase.
    lugartrabajo = models.CharField(db_column='LugarTrabajo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    referenciatrabajo = models.CharField(db_column='ReferenciaTrabajo', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    telefonofijotrabajo = models.CharField(db_column='TelefonoFijoTrabajo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    correoelectronicotrabajo = models.CharField(db_column='CorreoElectronicoTrabajo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    actualizado = models.BooleanField(db_column='Actualizado')  # Field name made lowercase.
    fechaactualizacion = models.DateTimeField(db_column='FechaActualizacion')  # Field name made lowercase.
    actualizadopor = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='ActualizadoPor')  # Field name made lowercase.
    agente = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='Agente', blank=True, null=True)  # Field name made lowercase.
    departamento = models.ForeignKey('Departamento', models.DO_NOTHING, db_column='Departamento', blank=True, null=True)  # Field name made lowercase.
    filial = models.ForeignKey('Filial', models.DO_NOTHING, db_column='Filial', blank=True, null=True)  # Field name made lowercase.
    municipio = models.ForeignKey('Municipio', models.DO_NOTHING, db_column='Municipio', blank=True, null=True)  # Field name made lowercase.
    sucursal = models.ForeignKey('Sucursal', models.DO_NOTHING, db_column='Sucursal', blank=True, null=True)  # Field name made lowercase.
    codigorechazo = models.IntegerField(db_column='CodigoRechazo', blank=True, null=True)  # Field name made lowercase.
    comentarios = models.CharField(db_column='Comentarios', max_length=155, blank=True, null=True)  # Field name made lowercase.
    antiguedadanios = models.IntegerField(db_column='AntiguedadAnios', blank=True, null=True)  # Field name made lowercase.
    antiguedadmeses = models.IntegerField(db_column='AntiguedadMeses', blank=True, null=True)  # Field name made lowercase.
    puesto = models.CharField(db_column='Puesto', max_length=50, blank=True, null=True)  # Field name made lowercase.
    telefonocelular2 = models.CharField(db_column='TelefonoCelular2', max_length=12, blank=True, null=True)  # Field name made lowercase.
    tipoempresa = models.ForeignKey('Tipoempresa', models.DO_NOTHING, db_column='TipoEmpresa', blank=True, null=True)  # Field name made lowercase.
    actualizado_core = models.NullBooleanField()
    codcliente = models.CharField(db_column='CodCliente', max_length=100)  # Field name made lowercase.
    numerorifa = models.IntegerField(db_column='NumeroRifa', blank=True, null=True)  # Field name made lowercase.
    actividadcliente = models.ForeignKey(ActividadesEconomicas, models.DO_NOTHING, db_column='ActividadCliente', blank=True, null=True)  # Field name made lowercase.
    profesioncliente = models.ForeignKey('Profesiones', models.DO_NOTHING, db_column='ProfesionCliente', blank=True, null=True)  # Field name made lowercase.
    concoopcel = models.NullBooleanField(db_column='ConCoopcel')  # Field name made lowercase.
    modificadopor = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='ModificadoPor', blank=True, null=True)  # Field name made lowercase.
    observacionrechazo = models.CharField(db_column='ObservacionRechazo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    enviadoproduccionpor = models.IntegerField(db_column='EnviadoProduccionPor', blank=True, null=True)  # Field name made lowercase.
    enviadoproduccionfecha = models.CharField(db_column='EnviadoProduccionFecha', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ClientesHistoricos'


class Clientesxdirecciones(models.Model):
    coddireccion = models.IntegerField(db_column='CodDireccion', primary_key=True)  # Field name made lowercase.
    codcliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='CodCliente')  # Field name made lowercase.
    codtipodirecciones = models.ForeignKey('Tiposdirecciones', models.DO_NOTHING, db_column='CodTipoDirecciones', blank=True, null=True)  # Field name made lowercase.
    coddepartamento = models.ForeignKey('Departamentos', models.DO_NOTHING, db_column='CodDepartamento', blank=True, null=True)  # Field name made lowercase.
    codmunicipio = models.ForeignKey('Municipios', models.DO_NOTHING, db_column='CodMunicipio', blank=True, null=True)  # Field name made lowercase.
    codcolonia = models.ForeignKey('Colonias', models.DO_NOTHING, db_column='CodColonia', blank=True, null=True)  # Field name made lowercase.
    direccion = models.TextField(db_column='Direccion', blank=True, null=True)  # Field name made lowercase.
    activo = models.NullBooleanField(db_column='Activo')  # Field name made lowercase.
    codclienteinterno = models.CharField(db_column='CodClienteInterno', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ClientesXDirecciones'


class Clientesxgestiones(models.Model):
    codgestion = models.IntegerField(db_column='CodGestion', primary_key=True)  # Field name made lowercase.
    codcliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='CodCliente', blank=True, null=True)  # Field name made lowercase.
    codtipogestion = models.ForeignKey('Tiposgestion', models.DO_NOTHING, db_column='CodTipoGestion', blank=True, null=True)  # Field name made lowercase.
    codresultadogestion = models.ForeignKey('Resultadogestion', models.DO_NOTHING, db_column='CodResultadoGestion', blank=True, null=True)  # Field name made lowercase.
    codtelefono = models.ForeignKey('Clientesxtelefono', models.DO_NOTHING, db_column='CodTelefono', blank=True, null=True)  # Field name made lowercase.
    observaciones = models.TextField(db_column='Observaciones', blank=True, null=True)  # Field name made lowercase.
    fechainicio = models.DateTimeField(db_column='FechaInicio', blank=True, null=True)  # Field name made lowercase.
    fechafinal = models.DateTimeField(db_column='FechaFinal', blank=True, null=True)  # Field name made lowercase.
    codagente = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='CodAgente', blank=True, null=True)  # Field name made lowercase.
    razon = models.CharField(db_column='Razon', max_length=150, blank=True, null=True)  # Field name made lowercase.
    resultadorazon = models.CharField(db_column='ResultadoRazon', max_length=150, blank=True, null=True)  # Field name made lowercase.
    nombrecontacto = models.CharField(db_column='NombreContacto', max_length=150, blank=True, null=True)  # Field name made lowercase.
    telefonocontacto = models.CharField(db_column='TelefonoContacto', max_length=20, blank=True, null=True)  # Field name made lowercase.
    devolverllamada = models.DateTimeField(db_column='DevolverLlamada', blank=True, null=True)  # Field name made lowercase.
    estatus_gestion = models.CharField(max_length=100, blank=True, null=True)
    name_gestor = models.CharField(max_length=100, blank=True, null=True)
    adjunto = models.CharField(db_column='Adjunto', max_length=150, blank=True, null=True)  # Field name made lowercase.
    bufete = models.IntegerField(db_column='Bufete', blank=True, null=True)  # Field name made lowercase.
    coddireccion = models.IntegerField(db_column='CodDireccion', blank=True, null=True)  # Field name made lowercase.
    nombretercero = models.CharField(db_column='NombreTercero', max_length=150, blank=True, null=True)  # Field name made lowercase.
    correoelectronico = models.CharField(db_column='CorreoElectronico', max_length=50, blank=True, null=True)  # Field name made lowercase.
    titulomensaje = models.CharField(db_column='TituloMensaje', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mensaje = models.TextField(db_column='Mensaje', blank=True, null=True)  # Field name made lowercase.
    codclienteinterno = models.CharField(db_column='CodClienteInterno', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechagestion = models.CharField(db_column='FechaGestion', max_length=10, blank=True, null=True)  # Field name made lowercase.
    montopromesa = models.DecimalField(db_column='MontoPromesa', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    minutos = models.IntegerField(db_column='Minutos', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ClientesXGestiones'


class Clientesxpromesapago(models.Model):
    codpromesa = models.IntegerField(db_column='CodPromesa', primary_key=True)  # Field name made lowercase.
    codcliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='CodCliente', blank=True, null=True)  # Field name made lowercase.
    codagente = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='CodAgente', blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=12, blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    fechagestion = models.DateTimeField(db_column='FechaGestion', blank=True, null=True)  # Field name made lowercase.
    nombreagente = models.CharField(db_column='NombreAgente', max_length=50, blank=True, null=True)  # Field name made lowercase.
    codclienteinterno = models.CharField(db_column='CodClienteInterno', max_length=50, blank=True, null=True)  # Field name made lowercase.
    montopromesa = models.DecimalField(db_column='MontoPromesa', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    codgestion = models.ForeignKey(Clientesxgestiones, models.DO_NOTHING, db_column='CodGestion', blank=True, null=True)  # Field name made lowercase.
    cuota = models.DecimalField(db_column='Cuota', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ClientesXPromesaPago'


class Clientesxtelefono(models.Model):
    codtelefono = models.IntegerField(db_column='CodTelefono', primary_key=True)  # Field name made lowercase.
    codcliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='CodCliente')  # Field name made lowercase.
    codtipotelefono = models.ForeignKey('Tipostelefonos', models.DO_NOTHING, db_column='CodTipoTelefono', blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=40, blank=True, null=True)  # Field name made lowercase.
    mensaje = models.NullBooleanField(db_column='Mensaje')  # Field name made lowercase.
    activo = models.NullBooleanField(db_column='Activo')  # Field name made lowercase.
    personareferida = models.CharField(db_column='PersonaReferida', max_length=100, blank=True, null=True)  # Field name made lowercase.
    codclienteinterno = models.CharField(db_column='CodClienteInterno', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ClientesXTelefono'


class Colonias(models.Model):
    codcolonia = models.IntegerField(db_column='CodColonia', primary_key=True)  # Field name made lowercase.
    codmunicipio = models.ForeignKey('Municipios', models.DO_NOTHING, db_column='CodMunicipio', blank=True, null=True)  # Field name made lowercase.
    desccolonia = models.CharField(db_column='DescColonia', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Colonias'


class Departamento(models.Model):
    nombre = models.CharField(db_column='Nombre', max_length=100)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Departamento'


class Departamentos(models.Model):
    coddepartamento = models.IntegerField(db_column='CodDepartamento', primary_key=True)  # Field name made lowercase.
    descdepartamento = models.CharField(db_column='DescDepartamento', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Departamentos'


class Empleados(models.Model):
    idempleados = models.IntegerField(db_column='IDEmpleados')  # Field name made lowercase.
    nombree = models.CharField(db_column='NombreE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    contrasena = models.CharField(db_column='Contrasena', max_length=255, blank=True, null=True)  # Field name made lowercase.
    privilegio = models.IntegerField(db_column='Privilegio', blank=True, null=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=150, blank=True, null=True)  # Field name made lowercase.
    extension = models.CharField(db_column='Extension', max_length=10, blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nombrecorto = models.CharField(db_column='NombreCorto', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipoe = models.CharField(db_column='TipoE', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Empleados'


class Estados(models.Model):
    codestado = models.IntegerField(db_column='CodEstado', primary_key=True)  # Field name made lowercase.
    descestado = models.CharField(db_column='DescEstado', max_length=75, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Estados'


class Filial(models.Model):
    codigo = models.CharField(db_column='Codigo', max_length=20)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=200)  # Field name made lowercase.
    referencia = models.CharField(db_column='Referencia', max_length=500, blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=10, blank=True, null=True)  # Field name made lowercase.
    departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='Departamento')  # Field name made lowercase.
    municipio = models.ForeignKey('Municipio', models.DO_NOTHING, db_column='Municipio')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Filial'


class Gestiones(models.Model):
    telefono = models.CharField(db_column='Telefono', max_length=12)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha')  # Field name made lowercase.
    horainicio = models.DateTimeField(db_column='HoraInicio')  # Field name made lowercase.
    horafinal = models.DateTimeField(db_column='HoraFinal')  # Field name made lowercase.
    agente = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='Agente')  # Field name made lowercase.
    tipogestion = models.IntegerField(db_column='TipoGestion')  # Field name made lowercase.
    clientelocalizado = models.ForeignKey(Clienteshistoricos, models.DO_NOTHING, db_column='ClienteLocalizado', blank=True, null=True)  # Field name made lowercase.
    clientenolocalizado = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='ClienteNoLocalizado', blank=True, null=True)  # Field name made lowercase.
    clientependiente = models.ForeignKey(Clientesactualizar, models.DO_NOTHING, db_column='ClientePendiente', blank=True, null=True)  # Field name made lowercase.
    codigocliente = models.IntegerField(db_column='CodigoCliente', blank=True, null=True)  # Field name made lowercase.
    identidadcliente = models.CharField(db_column='IdentidadCliente', max_length=15, blank=True, null=True)  # Field name made lowercase.
    clienterechazado = models.ForeignKey(Clienteshistoricos, models.DO_NOTHING, db_column='ClienteRechazado', blank=True, null=True)  # Field name made lowercase.
    devolverllamada = models.CharField(db_column='DevolverLlamada', max_length=40, blank=True, null=True)  # Field name made lowercase.
    nombrecontacto = models.CharField(db_column='NombreContacto', max_length=100, blank=True, null=True)  # Field name made lowercase.
    telefonocontacto = models.CharField(db_column='TelefonoContacto', max_length=12, blank=True, null=True)  # Field name made lowercase.
    fuerechazado = models.NullBooleanField(db_column='FueRechazado')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Gestiones'


class Globalparameters(models.Model):
    nombreempresa = models.CharField(db_column='NombreEmpresa', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GlobalParameters'


class Historialasignacion(models.Model):
    codhistorial = models.IntegerField(db_column='CodHistorial')  # Field name made lowercase.
    productos = models.TextField(db_column='Productos', blank=True, null=True)  # Field name made lowercase.
    agencias = models.TextField(db_column='Agencias', blank=True, null=True)  # Field name made lowercase.
    diasmora = models.CharField(db_column='DiasMora', max_length=100, blank=True, null=True)  # Field name made lowercase.
    capitalmora = models.CharField(db_column='CapitalMora', max_length=100, blank=True, null=True)  # Field name made lowercase.
    agente = models.IntegerField(db_column='Agente', blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    estado = models.SmallIntegerField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HistorialAsignacion'


class Logueos(models.Model):
    idlogeo = models.AutoField(db_column='IdLogeo')  # Field name made lowercase.
    usuarioid = models.CharField(db_column='UsuarioId', max_length=50, blank=True, null=True)  # Field name made lowercase.
    hora = models.DateTimeField(db_column='Hora', blank=True, null=True)  # Field name made lowercase.
    estado = models.IntegerField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.
    motivo = models.CharField(db_column='Motivo', max_length=150, blank=True, null=True)  # Field name made lowercase.
    observaciones = models.CharField(db_column='Observaciones', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Logueos'


class Motivo(models.Model):
    nombre = models.CharField(db_column='Nombre', max_length=30)  # Field name made lowercase.
    activo = models.NullBooleanField(db_column='Activo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Motivo'


class Municipio(models.Model):
    nombre = models.CharField(db_column='Nombre', max_length=100)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='Departamento')  # Field name made lowercase.
    codmunicipio = models.IntegerField(db_column='CodMunicipio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Municipio'


class Municipios(models.Model):
    codmunicipio = models.IntegerField(db_column='CodMunicipio', primary_key=True)  # Field name made lowercase.
    coddepartamento = models.ForeignKey(Departamentos, models.DO_NOTHING, db_column='CodDepartamento', blank=True, null=True)  # Field name made lowercase.
    descmunicipio = models.CharField(db_column='DescMunicipio', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Municipios'


class Profesiones(models.Model):
    codigo_profesion = models.AutoField(db_column='CODIGO_PROFESION', primary_key=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='DESCRIPCION', max_length=60, blank=True, null=True)  # Field name made lowercase.
    activo_b = models.CharField(db_column='ACTIVO_B', max_length=1, blank=True, null=True)  # Field name made lowercase.
    creado_por = models.CharField(db_column='CREADO_POR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fecha_creacion = models.DateTimeField(db_column='FECHA_CREACION', blank=True, null=True)  # Field name made lowercase.
    modificado_por = models.CharField(db_column='MODIFICADO_POR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fecha_modificacion = models.DateTimeField(db_column='FECHA_MODIFICACION', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PROFESIONES'


class Productoscredito(models.Model):
    codproducto = models.IntegerField(db_column='CodProducto')  # Field name made lowercase.
    nombrecorto = models.CharField(db_column='NombreCorto', max_length=30)  # Field name made lowercase.
    nombrelargo = models.CharField(db_column='NombreLargo', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ProductosCredito'


class Reclamos(models.Model):
    codreclamo = models.IntegerField(db_column='CodReclamo', primary_key=True)  # Field name made lowercase.
    codcliente = models.IntegerField(db_column='CodCliente', blank=True, null=True)  # Field name made lowercase.
    numeroidentidad = models.CharField(db_column='NumeroIdentidad', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechahora = models.DateTimeField(db_column='FechaHora', blank=True, null=True)  # Field name made lowercase.
    codcategoria = models.ForeignKey(Categorias, models.DO_NOTHING, db_column='CodCategoria', blank=True, null=True)  # Field name made lowercase.
    codtiporeclamo = models.ForeignKey('Tiposreclamo', models.DO_NOTHING, db_column='CodTipoReclamo', blank=True, null=True)  # Field name made lowercase.
    ref1 = models.CharField(db_column='Ref1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ref2 = models.CharField(db_column='Ref2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ref3 = models.CharField(db_column='Ref3', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ref4 = models.CharField(db_column='Ref4', max_length=100, blank=True, null=True)  # Field name made lowercase.
    observaciones = models.CharField(db_column='Observaciones', max_length=500, blank=True, null=True)  # Field name made lowercase.
    oficialingresa = models.IntegerField(db_column='OficialIngresa', blank=True, null=True)  # Field name made lowercase.
    oficialasignado = models.IntegerField(db_column='OficialAsignado', blank=True, null=True)  # Field name made lowercase.
    escalado = models.NullBooleanField(db_column='Escalado')  # Field name made lowercase.
    codestado = models.ForeignKey(Estados, models.DO_NOTHING, db_column='CodEstado', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Reclamos'


class Resultadogestion(models.Model):
    codresultadogestion = models.IntegerField(db_column='CodResultadoGestion', primary_key=True)  # Field name made lowercase.
    descresultadogestion = models.CharField(db_column='DescResultadoGestion', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ResultadoGestion'


class Sucursal(models.Model):
    nombre = models.CharField(db_column='Nombre', max_length=100)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', max_length=20)  # Field name made lowercase.
    codmapadepartamento = models.DecimalField(db_column='CodMapaDepartamento', max_digits=18, decimal_places=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sucursal'


class Temporal1(models.Model):
    codigo_credito = models.CharField(max_length=255, blank=True, null=True)
    codigo_cliente = models.CharField(max_length=255, blank=True, null=True)
    cliente_id = models.CharField(max_length=255, blank=True, null=True)
    nombre_cliente = models.CharField(max_length=255, blank=True, null=True)
    sexo = models.CharField(max_length=255, blank=True, null=True)
    correo_electronico = models.CharField(max_length=255, blank=True, null=True)
    dias_mora = models.CharField(max_length=255, blank=True, null=True)
    proxima_fecha_pago = models.CharField(max_length=255, blank=True, null=True)
    cuotas_mora = models.CharField(max_length=255, blank=True, null=True)
    capital_mora = models.CharField(max_length=255, blank=True, null=True)
    intereses_mora = models.CharField(max_length=255, blank=True, null=True)
    intereses_moratorios = models.CharField(max_length=255, blank=True, null=True)
    otros_cargos = models.CharField(max_length=255, blank=True, null=True)
    total = models.CharField(max_length=255, blank=True, null=True)
    identidad = models.CharField(max_length=255, blank=True, null=True)
    cuenta = models.CharField(max_length=255, blank=True, null=True)
    producto = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Temporal1'


class Temporal2(models.Model):
    codigo_credito = models.CharField(max_length=30)
    codigo_cliente = models.CharField(max_length=10)
    cliente_id = models.BigIntegerField()
    nombre_cliente = models.CharField(max_length=255)
    sexo = models.CharField(max_length=30, blank=True, null=True)
    correo_electronico = models.CharField(max_length=100)
    dias_mora = models.IntegerField(blank=True, null=True)
    proxima_fecha_pago = models.CharField(max_length=10, blank=True, null=True)
    cuotas_mora = models.IntegerField(blank=True, null=True)
    capital_mora = models.DecimalField(max_digits=38, decimal_places=2, blank=True, null=True)
    intereses_mora = models.DecimalField(max_digits=38, decimal_places=2, blank=True, null=True)
    intereses_moratorios = models.DecimalField(max_digits=18, decimal_places=2)
    otros_cargos = models.DecimalField(max_digits=30, decimal_places=7, blank=True, null=True)
    total = models.DecimalField(max_digits=38, decimal_places=2, blank=True, null=True)
    identidad = models.CharField(max_length=30)
    cuenta = models.CharField(max_length=30, blank=True, null=True)
    producto = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'Temporal2'


class Tipoacciones(models.Model):
    codtipoacciones = models.IntegerField(db_column='CodTipoAcciones', primary_key=True)  # Field name made lowercase.
    desctipoacciones = models.CharField(db_column='DescTipoAcciones', max_length=75, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TipoAcciones'


class Tipoempresa(models.Model):
    nombre = models.CharField(db_column='Nombre', max_length=100)  # Field name made lowercase.
    activo = models.BooleanField(db_column='Activo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TipoEmpresa'


class Tiposdirecciones(models.Model):
    codtipodirecciones = models.IntegerField(db_column='CodTipoDirecciones', primary_key=True)  # Field name made lowercase.
    desctipotdirecciones = models.CharField(db_column='DescTipoTDirecciones', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TiposDirecciones'


class Tiposestados(models.Model):
    codestado = models.IntegerField(db_column='CodEstado', primary_key=True)  # Field name made lowercase.
    descestado = models.CharField(db_column='DescEstado', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TiposEstados'


class Tiposgestion(models.Model):
    codtipogestion = models.IntegerField(db_column='CodTipoGestion', primary_key=True)  # Field name made lowercase.
    desctipogestion = models.CharField(db_column='DescTipoGestion', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TiposGestion'


class Tipospestanas(models.Model):
    codpestana = models.IntegerField(db_column='CodPestana', primary_key=True)  # Field name made lowercase.
    descpestana = models.CharField(db_column='DescPestana', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TiposPestanas'


class Tiposreclamo(models.Model):
    codtiporeclamo = models.IntegerField(db_column='CodTipoReclamo', primary_key=True)  # Field name made lowercase.
    codcategoria = models.ForeignKey(Categorias, models.DO_NOTHING, db_column='CodCategoria', blank=True, null=True)  # Field name made lowercase.
    desccategoria = models.CharField(db_column='DescCategoria', max_length=75, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TiposReclamo'


class Tipostelefonos(models.Model):
    codtipotelefono = models.IntegerField(db_column='CodTipoTelefono', primary_key=True)  # Field name made lowercase.
    desctipotelefono = models.CharField(db_column='DescTipoTelefono', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TiposTelefonos'


class Zonaagencia(models.Model):
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    region = models.CharField(db_column='Region', max_length=255, blank=True, null=True)  # Field name made lowercase.
    agencia = models.CharField(db_column='Agencia', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ZonaAgencia'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128)
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)
