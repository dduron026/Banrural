from __future__ import unicode_literals

from django.db import models

class Estados(models.Model):
    codigo = models.AutoField(db_column='CodEstado', primary_key=True)
    nombre = models.CharField(db_column='DescEstado', max_length=75, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Rec].[Estados'

    def __unicode__(self):
		return '%s'%(self.nombre)

class TipoAcciones(models.Model):
    codigo = models.AutoField(db_column='CodTipoAcciones', primary_key=True)
    nombre = models.CharField(db_column='DescTipoAcciones', max_length=75, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Rec].[TipoAcciones'

    def __unicode__(self):
		return '%s'%(self.nombre)

class Categorias(models.Model):
    codigo = models.AutoField(db_column='CodCategoria', primary_key=True)
    nombre = models.CharField(db_column='DescCategoria', max_length=75, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Rec].[Categorias'

    def __unicode__(self):
		return '%s'%(self.nombre)

class TiposReclamo(models.Model):
    codigo = models.AutoField(db_column='CodTipoReclamo', primary_key=True)
    categoria = models.ForeignKey(Categorias, models.DO_NOTHING, db_column='CodCategoria', blank=True, null=True)
    nombre = models.CharField(db_column='DescCategoria', max_length=75, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Rec].[TiposReclamo'

    def __unicode__(self):
		return '%s'%(self.nombre)

class Reclamos(models.Model):
    reclamo = models.AutoField(db_column='CodReclamo', primary_key=True)
    cliente = models.IntegerField(db_column='CodCliente', blank=True, null=True)
    identidad = models.CharField(db_column='NumeroIdentidad', max_length=50, blank=True, null=True)
    fecha_hora = models.DateTimeField(db_column='FechaHora', blank=True, null=True, auto_now_add=True)
    categoria = models.ForeignKey(Categorias, models.DO_NOTHING, db_column='CodCategoria', blank=True, null=True)
    tipo_reclamo = models.ForeignKey('TiposReclamo', models.DO_NOTHING, db_column='CodTipoReclamo', blank=True, null=True)
    ref1 = models.CharField(db_column='Ref1', max_length=100, blank=True, null=True)
    ref2 = models.CharField(db_column='Ref2', max_length=100, blank=True, null=True)
    ref3 = models.CharField(db_column='Ref3', max_length=100, blank=True, null=True)
    ref4 = models.CharField(db_column='Ref4', max_length=100, blank=True, null=True)
    observaciones = models.CharField(db_column='Observaciones', max_length=500, blank=True, null=True)
    oficial_ingresa = models.IntegerField(db_column='OficialIngresa', blank=True, null=True)
    oficial_asignado = models.IntegerField(db_column='OficialAsignado', blank=True, null=True)
    escalado = models.NullBooleanField(db_column='Escalado')
    estado = models.ForeignKey(Estados, models.DO_NOTHING, db_column='CodEstado', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Rec].[Reclamos'

    def __unicode__(self):
		return '%s'%(self.identidad)

class Acciones(models.Model):
    codigo = models.AutoField(db_column='CodAccion', primary_key=True)
    reclamo = models.ForeignKey('Reclamos', models.DO_NOTHING, db_column='CodReclamo', blank=True, null=True)
    orden_nominal = models.IntegerField(db_column='OrdenNominal', blank=True, null=True)
    fecha_hora = models.DateTimeField(db_column='FechaHora', blank=True, null=True)
    oficial_accion = models.IntegerField(db_column='OficialAccion', blank=True, null=True)
    tipo_acciones = models.ForeignKey('Tipoacciones', models.DO_NOTHING, db_column='CodTipoAcciones', blank=True, null=True)
    observaciones = models.CharField(db_column='Observaciones', max_length=500, blank=True, null=True)
    adjunto = models.CharField(db_column='Adjunto', max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Rec].[Acciones'


