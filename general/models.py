from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Departamento(models.Model):
    nombre = models.CharField(db_column='Nombre', max_length=100)
    codigo = models.CharField(db_column='Codigo', max_length=10, blank=True, null=True)
    class Meta:
        db_table = 'Departamento'
    def __unicode__(self):
        return u'%s' % (self.nombre)

class Municipio(models.Model):
    departamento = models.ForeignKey(Departamento,db_column='Departamento')
    nombre = models.CharField(db_column='Nombre', max_length=100)
    codigo = models.CharField(db_column='Codigo', max_length=10, blank=True, null=True)
    class Meta:
        db_table = 'Municipio'
    def __unicode__(self):
        return u'%s' % (self.nombre)


class Filial(models.Model):
    codigo = models.CharField(db_column='Codigo', max_length=20)
    nombre = models.CharField(db_column='Nombre', max_length=200)
    departamento = models.ForeignKey(Departamento, db_column='Departamento')
    municipio = models.ForeignKey(Municipio,db_column='Municipio' )
    referencia = models.CharField(db_column='Referencia', max_length=500, blank=True, null=True)
    telefono = models.CharField(db_column='Telefono', max_length=10, blank=True, null=True) 
    class Meta:
        db_table = 'Filial'
    def __unicode__(self):
        return u'%s' % (self.nombre)

class Motivo(models.Model):
    nombre = models.CharField(db_column='Nombre', max_length=30)
    activo = models.NullBooleanField(db_column='Activo', )
    class Meta:
        db_table = 'Motivo'
    def __unicode__(self):
        return u'%s' % (self.nombre)

class TipoEmpresa(models.Model):
    nombre = models.CharField(db_column='Nombre', max_length=100)
    activo = models.BooleanField(db_column='Activo', default=True)
    class Meta:
        db_table = 'TipoEmpresa'
    def __unicode__(self):
        return u'%s' % (self.nombre)

class Sucursal(models.Model):
    nombre = models.CharField(db_column='Nombre', max_length=100)
    codmapa_deptartamento = models.DecimalField(db_column='CodMapaDepartamento', max_digits=18, decimal_places=1)
    codigo = models.CharField(db_column='Codigo', max_length=20)

    class Meta:
        db_table = 'Sucursal'
    def __unicode__(self):
        return u'%s' % (self.nombre)

class Logueos(models.Model):
    usuarioid = models.ForeignKey(User, db_column='UsuarioId', blank=True, null=True)
    hora = models.DateTimeField(db_column='Hora', null=True)
    estado = models.IntegerField(db_column = 'Estado',null = True)
    motivo = models.CharField(db_column='Motivo', max_length=150)
    observaciones = models.CharField(db_column='Observaciones', max_length=250)

    class Meta:
        managed = False
        db_table = 'Logueos'

    def __unicode__(self):
        return self.usuarioid