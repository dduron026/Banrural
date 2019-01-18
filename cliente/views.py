# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import *
from django.template import RequestContext
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from cliente.forms import *
from django.db import transaction, IntegrityError
from django.db.models import Count, CharField, Case, Value, When
from django.db import connection
from django.utils import timezone

import time
import datetime
import json
def date_handler(obj):
	if hasattr(obj, 'isoformat'):
		return obj.isoformat()
	else:
		raise TypeError

@login_required()
@transaction.atomic
def actualizar_callcenter(request):
	gest= Gestion.objects.filter(cliente_pendiente__isnull=False, devolver_llamada__isnull=False, agente=request.user)
	recordatorios = []
	for gestion in gest:
		fecha = datetime.datetime.today()
		date_object = datetime.datetime.strptime(gestion.devolver_llamada+'.000000', '%Y-%m-%d %H:%M:%S.%f')
		if fecha >= date_object:
			recordatorios.append({'cliente': gestion.cliente_pendiente.primer_nombre+ ' ' + gestion.cliente_pendiente.primer_apellido , 'fecha': date_object.strftime('%Y-%m-%d %I:%M:%S%p')})

	gestiones = Gestion.objects.values(
		'agente',
		'agente__first_name', 
		'agente__last_name'
	).filter(fecha= datetime.date.today(), agente=request.user).annotate(
		total_localizado=Count('cliente_localizado'), 
		total_no_localizado=Count('cliente_no_localizado'), 
		total_pendiente=Count('cliente_pendiente'), 
		total=Count('agente')
	)
	if request.is_ajax():
		id = request.GET['id']
		try:
			if request.GET.get('metodo') != '' and request.GET.get('metodo') != None:
				persona = dict(
					ClienteHistorico.objects.values(
						'id',
						'codigo',
						'identidad',
						'primer_nombre',
						'primer_apellido',
						'segundo_apellido',
						'sexo',
						'estado_civil',
						'departamento',
						'municipio',
						'colonia',
						'referencia',
						'telefono_fijo',
						'telefono_celular',
						'correo_electronico',
						'profesion',
						'ingresos',
						'monto_cuentas',
						'departamento_trabajo',
						'municipio_trabajo',
						'lugar_trabajo',
						'referencia_trabajo',
						'telefono_fijo_trabajo',
						'correo_electronico_trabajo',
						'actualizado',
						'sucursal',
						'agente',
						'filial',
						'actualizado_por',
						'fecha_actualizacion',
						'codigo_rechazo',
						'comentarios',
						'telefono_celular2',
						'tipo_empresa',
						'puesto',
						'antiguedad_anios',
						'antiguedad_meses',
						'rifa',
						'profesion_cliente',
						'actividad_cliente',
						'actualizado_core',
						'con_coopcel',
					).get(id=id)
				)
			else:
				persona = dict(
					ClienteActualizar.objects.values(
						'codigo',
						'primer_nombre',
						'primer_apellido', 
						'segundo_apellido', 
						'sexo', 
						'correo_electronico',
						'telefono_fijo',
						'telefono_celular',
						'identidad',
						'con_coopcel'
					).get(id=id)
				)
			gestiones = list(
				Gestion.objects.values(
					'agente__first_name',
					'agente__last_name',
					'fecha',
					'hora_incio',
					'telefono',
					'tipo_gestion'
				).filter(cliente=persona['codigo'])
			)
			print gestiones
		except Exception, e:
			print e
			persona = False
			gestiones = False

		data = {
			'gestiones': gestiones,
			'persona': persona
		}

		return HttpResponse(json.dumps(data, default=date_handler), content_type='application/json')
	elif request.method == 'GET':
		clientes = ClienteActualizar.objects.filter(agente=request.user, actualizado=False, codigo_rechazo__isnull= True, gestion__cliente_pendiente__isnull=True).order_by('-fecha_actualizacion')[:5]
		clientes_pendientes = Gestion.objects.filter(cliente_pendiente__isnull=False, agente=request.user).exclude(devolver_llamada__isnull=True).extra({'fecha_cast': "CAST(DevolverLlamada as DATE)"}).order_by('fecha_cast')[:5]
		clientes_rechazados = Gestion.objects.filter(cliente_rechazado__isnull=False, agente=request.user).order_by('-hora_final')[:5]
		
		formulario = ClienteActualizarForm()
		formulario2 = ClienteHistoricoForm()
		ctx={
			'formulario': formulario,
			'formulario2': formulario2,
			'clientes': clientes,
			'clientes_pendientes': clientes_pendientes,
			'clientes_rechazados': clientes_rechazados,
			'gestiones': gestiones,
			'recordatorios': recordatorios,
		}
		return render(request, 'actualizar_cliente_callcenter.html', ctx)
	elif request.method == 'POST':
		rifa = False
		if request.POST['metodo'] == 'actualizar':
			cliente = ClienteActualizar.objects.get(id=request.POST['modal-localizado-cliente'])
			if int(request.POST['tipo-gestion']) == 3:
				fecha = datetime.datetime.today()
				unida = "%s-%s-%s %s" % (fecha.year, fecha.month, fecha.day,  request.POST['hora-inicio']) 
				
				try:
					gestiones_anteriores = Gestion.objects.filter(cliente_pendiente=cliente)
					gestiones_anteriores.delete() 
				except Exception, e:
					pass

				gestion = Gestion()
				gestion.agente = request.user
				gestion.cliente_pendiente = cliente
				gestion.telefono = request.POST['telefono']
				gestion.hora_incio = unida
				gestion.tipo_gestion = 3
				gestion.identidad = cliente.identidad
				gestion.cliente = cliente.id
				gestion.save()
			elif int(request.POST['tipo-gestion']) == 4:
				cliente = ClienteActualizar.objects.get(id=request.POST['modal-localizado-cliente'])
				try:
					gestiones_anteriores = Gestion.objects.filter(cliente_pendiente=cliente)
					gestiones_anteriores.delete() 
				except Exception, e:
					pass

				try:
					with transaction.atomic():
						cliente.actualizado_por = request.user
						cliente.actualizado = True
						cliente.agente = request.user
						cliente.save()


						actualizar = Cliente()
						actualizar.identidad = cliente.identidad
						actualizar.primer_nombre = cliente.primer_nombre
						actualizar.primer_apellido = cliente.primer_apellido
						actualizar.segundo_apellido = cliente.segundo_apellido
						actualizar.sexo = cliente.sexo
					
						actualizar.estado_civil = cliente.estado_civil
						actualizar.codigo = cliente.id
						actualizar.departamento = cliente.departamento
						actualizar.municipio = cliente.municipio
						actualizar.colonia = cliente.colonia
						actualizar.referencia = cliente.referencia
						actualizar.telefono_fijo = cliente.telefono_fijo
						actualizar.telefono_celular = cliente.telefono_celular
						actualizar.correo_electronico = cliente.correo_electronico
						actualizar.profesion = cliente.profesion
						actualizar.ingresos = cliente.ingresos
						actualizar.monto_cuentas = cliente.monto_cuentas
						actualizar.departamento_trabajo = cliente.departamento_trabajo
						actualizar.municipio_trabajo = cliente.municipio_trabajo
						actualizar.lugar_trabajo = cliente.lugar_trabajo
						actualizar.referencia_trabajo = cliente.referencia_trabajo
						actualizar.telefono_fijo_trabajo = cliente.telefono_fijo_trabajo
						actualizar.correo_electronico_trabajo = cliente.correo_electronico_trabajo
						actualizar.actualizado_por = request.user
						actualizar.con_coopcel = cliente.con_coopcel
						actualizar.actividad_cliente = cliente.actividad_cliente
						actualizar.profesion_cliente = cliente.profesion_cliente
						actualizar.agente = request.user
						actualizar.save()
						

						fecha = datetime.date.today()
						unida = "%s-%s-%s %s" % (fecha.year, fecha.month, fecha.day,  request.POST['hora-inicio']) 
						gestion = Gestion()
						gestion.agente = request.user
						gestion.cliente_no_localizado = actualizar
						gestion.telefono = request.POST['telefono']
						gestion.hora_incio = timezone.now()
						gestion.tipo_gestion = 4
						gestion.identidad = cliente.identidad
						gestion.cliente = cliente.id
						gestion.save()

				except Exception, e:
					print e
					pass
			else:
				formulario = ClienteActualizarForm(request.POST, instance=cliente)
				formulario2 = ClienteForm(request.POST)
				if formulario.is_valid():
					try:
						try:
							gestiones_anteriores = Gestion.objects.filter(cliente_pendiente=cliente)
							gestiones_anteriores.delete() 
						except Exception, e:
							pass

						with transaction.atomic():
							try:
								cliente_actualizar = ClienteGeneral.objects.get(identidad=cliente.identidad)
								cliente_actualizar.actualizado = True
								cliente_actualizar.actualizado_por = request.user
								cliente_actualizar.agente = request.user
								cliente_actualizar.save()
							except Exception, e:
								pass
								
							cliente = ClienteActualizar.objects.get(id=request.POST['modal-localizado-cliente'])
							cliente.actualizado = True
							cliente.actualizado_por = request.user
							cliente.agente = request.user
							cliente.save()


							actualizar = formulario2.save(commit=False)
							actualizar.identidad = cliente.identidad
							actualizar.primer_nombre = cliente.primer_nombre
							actualizar.primer_apellido = cliente.primer_apellido
							actualizar.segundo_apellido = cliente.segundo_apellido
							actualizar.sexo = cliente.sexo
							actualizar.codigo = cliente.codigo	
						
							actualizar.estado_civil = cliente.estado_civil
							actualizar.departamento = cliente.departamento
							actualizar.municipio = cliente.municipio
							actualizar.colonia = cliente.colonia
							actualizar.referencia = cliente.referencia
							actualizar.telefono_fijo = cliente.telefono_fijo
							actualizar.telefono_celular = cliente.telefono_celular
							actualizar.correo_electronico = cliente.correo_electronico
							actualizar.profesion = cliente.profesion
							actualizar.ingresos = cliente.ingresos
							actualizar.monto_cuentas = cliente.monto_cuentas
							actualizar.departamento_trabajo = cliente.departamento_trabajo
							actualizar.municipio_trabajo = cliente.municipio_trabajo
							actualizar.lugar_trabajo = cliente.lugar_trabajo
							actualizar.referencia_trabajo = cliente.referencia_trabajo
							actualizar.telefono_fijo_trabajo = cliente.telefono_fijo_trabajo
							actualizar.correo_electronico_trabajo = cliente.correo_electronico_trabajo
							actualizar.sucursal = cliente.sucursal
							actualizar.agente = request.user
							actualizar.filial = cliente.filial
							actualizar.actualizado_por = request.user
							actualizar.codigo_rechazo = cliente.codigo_rechazo
							actualizar.comentarios = cliente.comentarios
							actualizar.actualizado = True
							actualizar.codigo = cliente.codigo
							actualizar.con_coopcel = cliente.con_coopcel
							actualizar.actividad_cliente = cliente.actividad_cliente
							actualizar.profesion_cliente = cliente.profesion_cliente
							actualizar.save()


							registro = formulario.save(commit=False)
							historico = ClienteHistorico()
						
							historico.identidad = registro.identidad
							historico.primer_nombre = registro.primer_nombre
							historico.primer_apellido = registro.primer_apellido
							historico.segundo_apellido = registro.segundo_apellido
							historico.sexo = registro.sexo
							historico.codigo = registro.codigo

							historico.estado_civil = cliente.estado_civil if registro.estado_civil == '' or registro.estado_civil == None else registro.estado_civil  
							historico.departamento = cliente.departamento if registro.departamento == '' or registro.departamento == None else registro.departamento 
							historico.municipio = cliente.municipio if request.POST.get('municipio') == '' or request.POST.get('municipio_trabajo') == None else Municipio.objects.get(pk=request.POST.get('municipio'))
							historico.colonia = cliente.colonia if registro.colonia == '' or registro.colonia == None else registro.colonia
							historico.referencia = cliente.referencia if registro.referencia == '' or registro.referencia == None else registro.referencia
							historico.telefono_fijo = cliente.telefono_fijo if registro.telefono_fijo == '' or registro.telefono_fijo == None else registro.telefono_fijo
							historico.telefono_celular = cliente.telefono_celular if registro.telefono_celular == '' or registro.telefono_celular == None else registro.telefono_celular
							historico.telefono_celular2 = None if request.POST.get('telefono_celular2') == '' else request.POST.get('telefono_celular2') 
							historico.correo_electronico =  cliente.correo_electronico if registro.correo_electronico == '' or registro.correo_electronico == None else registro.correo_electronico
							historico.profesion_cliente = cliente.profesion_cliente if request.POST.get('profesion_cliente') == '' else Profesion.objects.get(codigo_profesion=request.POST.get('profesion_cliente'))

							historico.ingresos = cliente.ingresos if registro.ingresos == '' else registro.ingresos
							historico.monto_cuentas = cliente.monto_cuentas if registro.monto_cuentas == '' else registro.monto_cuentas 
							historico.departamento_trabajo = cliente.departamento_trabajo if registro.departamento_trabajo == '' or registro.departamento_trabajo == None else registro.departamento_trabajo
							historico.municipio_trabajo = cliente.municipio_trabajo if request.POST.get('municipio_trabajo') == '' or request.POST.get('municipio_trabajo') == None else Municipio.objects.get(pk=request.POST.get('municipio_trabajo'))
							historico.lugar_trabajo = cliente.lugar_trabajo if registro.lugar_trabajo == '' or registro.lugar_trabajo == None else registro.lugar_trabajo
							historico.referencia_trabajo = cliente.referencia_trabajo if registro.referencia_trabajo == '' or registro.referencia_trabajo == None else registro.referencia_trabajo
							historico.telefono_fijo_trabajo = cliente.telefono_fijo_trabajo if registro.telefono_fijo_trabajo == '' or registro.telefono_fijo_trabajo == None else registro.telefono_fijo_trabajo
							historico.correo_electronico_trabajo = cliente.correo_electronico_trabajo if registro.correo_electronico_trabajo == '' or registro.correo_electronico_trabajo == None else registro.correo_electronico_trabajo
							
							historico.tipo_empresa = None if request.POST.get('tipo_empresa') == '' or request.POST.get('tipo_empresa') == None else TipoEmpresa.objects.get(id=request.POST.get('tipo_empresa'))
							historico.actividad_cliente =  cliente.actividad_cliente if request.POST.get('actividad_cliente') == '' or request.POST.get('actividad_cliente') == None else ActividadEconomica.objects.get(codigo_actividad_economica=request.POST.get('actividad_cliente'))
							historico.puesto = None if request.POST.get('puesto') == '' else request.POST.get('puesto')
							historico.antiguedad_anios = None if request.POST.get('antiguedad_anios') == '' else request.POST.get('antiguedad_anios') 
							historico.antiguedad_meses = None if request.POST.get('antiguedad_meses') == '' else request.POST.get('antiguedad_meses') 
							
							historico.actualizado = True
							historico.sucursal = registro.sucursal
							historico.agente = request.user
							historico.filial = registro.filial
							historico.actualizado_por = request.user
							historico.modificado_por = request.user
							historico.codigo_rechazo = registro.codigo_rechazo
							historico.con_coopcel = cliente.con_coopcel
							historico.comentarios = registro.comentarios

							historico.save()

							with connection.cursor() as cursor:
								cursor.execute("SELECT NEXT VALUE FOR SorteoIdSecuencia AS secuencia;")
								row = cursor.fetchone()
							
							historico.rifa = row[0]
							historico.save()
							
							print row
							fecha = datetime.datetime.today()
							unida = "%s-%s-%s %s" % (fecha.year, fecha.month, fecha.day,  request.POST['hora-inicio']) 

							gestion = Gestion()
							gestion.agente = request.user
							gestion.cliente_localizado = historico
							gestion.telefono = request.POST['telefono']
							gestion.hora_incio = unida
							gestion.tipo_gestion = 1
							gestion.identidad = registro.identidad
							gestion.cliente = registro.codigo
							gestion.save()

							rifa = {
								'identidad': historico.identidad,
								'nombres' : "%s %s %s" % (historico.primer_nombre, historico.primer_apellido, historico.segundo_apellido),
								'numero' : historico.rifa
							}

					except Exception, e:
						raise e
				else:
					print formulario.errors

			formulario = ClienteActualizarForm()
			formulario2 = ClienteHistoricoForm()
			clientes = ClienteActualizar.objects.filter(agente=request.user, actualizado=False, codigo_rechazo__isnull= True, gestion__cliente_pendiente__isnull=True).order_by('-fecha_actualizacion')[:5]
			clientes_pendientes = Gestion.objects.filter(cliente_pendiente__isnull=False, agente=request.user).exclude(devolver_llamada__isnull=True).extra({'fecha_cast': "CAST(DevolverLlamada as DATE)"}).order_by('fecha_cast')[:5]
			clientes_rechazados = Gestion.objects.filter(cliente_rechazado__isnull=False, agente=request.user).order_by('-hora_final')[:5]
			ctx={
				'formulario': formulario,
				'formulario2': formulario2,
				'clientes': clientes,
				'clientes_pendientes': clientes_pendientes,
				'clientes_rechazados': clientes_rechazados,
				'gestiones': gestiones,
				'recordatorios': recordatorios,
				'rifa' : rifa
			}
			return render(request, 'actualizar_cliente_callcenter.html', ctx)
		elif request.POST['metodo'] == 'no-localizado':
			cliente = ClienteActualizar.objects.get(id=request.POST['modal-no-localizado-cliente'])
			try:
				try:
					gestiones_anteriores = Gestion.objects.filter(cliente_pendiente=cliente)
					gestiones_anteriores.delete() 
				except Exception, e:
					pass

				with transaction.atomic():
					cliente.codigo_rechazo = request.POST['razon']
					cliente.comentarios = request.POST['comentarios']
					cliente.codigo = cliente.id
					cliente.actualizado_por = request.user
					cliente.agente = request.user
					cliente.save()

					actualizar = Cliente()
					actualizar.identidad = cliente.identidad
					actualizar.primer_nombre = cliente.primer_nombre
					actualizar.primer_apellido = cliente.primer_apellido
					actualizar.segundo_apellido = cliente.segundo_apellido
					actualizar.sexo = cliente.sexo
					actualizar.codigo = cliente.id
				
					actualizar.estado_civil = cliente.estado_civil
					actualizar.departamento = cliente.departamento
					actualizar.municipio = cliente.municipio
					actualizar.colonia = cliente.colonia
					actualizar.referencia = cliente.referencia
					actualizar.telefono_fijo = cliente.telefono_fijo
					actualizar.telefono_celular = cliente.telefono_celular
					actualizar.correo_electronico = cliente.correo_electronico
					actualizar.profesion = cliente.profesion

					actualizar.ingresos = cliente.ingresos

					actualizar.monto_cuentas = cliente.monto_cuentas
					actualizar.departamento_trabajo = cliente.departamento_trabajo
					actualizar.municipio_trabajo = cliente.municipio_trabajo
					actualizar.lugar_trabajo = cliente.lugar_trabajo
					actualizar.referencia_trabajo = cliente.referencia_trabajo
					actualizar.telefono_fijo_trabajo = cliente.telefono_fijo_trabajo
					actualizar.correo_electronico_trabajo = cliente.correo_electronico_trabajo	
					actualizar.codigo_rechazo = request.POST['razon']
					actualizar.comentarios = request.POST['comentarios']
					actualizar.actualizado_por = request.user
					actualizar.agente = request.user
					actualizar.con_coopcel = cliente.con_coopcel

					actualizar.actividad_cliente = cliente.actividad_cliente
					actualizar.profesion_cliente = cliente.profesion_cliente
					actualizar.save()
					
					fecha = datetime.datetime.today()
					unida = "%s-%s-%s %s" % (fecha.year, fecha.month, fecha.day,  request.POST['hora-inicio']) 

					gestion = Gestion()
					gestion.agente = request.user
					gestion.cliente_no_localizado = actualizar
					gestion.telefono = request.POST['telefono']
					gestion.hora_incio = unida
					gestion.tipo_gestion = 2
					gestion.identidad = cliente.identidad
					gestion.cliente = cliente.id
					gestion.save()

			except Exception, e:
				pass


			formulario = ClienteActualizarForm()
			formulario2 = ClienteHistoricoForm()
			clientes = ClienteActualizar.objects.filter(agente=request.user, actualizado=False, codigo_rechazo__isnull= True, gestion__cliente_pendiente__isnull=True).order_by('-fecha_actualizacion')[:5]
			clientes_pendientes = Gestion.objects.filter(cliente_pendiente__isnull=False, agente=request.user).exclude(devolver_llamada__isnull=True).extra({'fecha_cast': "CAST(DevolverLlamada as DATE)"}).order_by('fecha_cast')[:5]
		
			clientes_rechazados = Gestion.objects.filter(cliente_rechazado__isnull=False, agente=request.user).order_by('-hora_final')[:5]
			ctx={
				'formulario': formulario,
				'formulario2': formulario2,
				'clientes': clientes,
				'clientes_pendientes': clientes_pendientes,
				'clientes_rechazados': clientes_rechazados,
				'gestiones': gestiones,
				'recordatorios': recordatorios,
			}
			return render(request, 'actualizar_cliente_callcenter.html', ctx)		
		elif request.POST['metodo'] == 'rechazado':
			cliente_id = request.POST.get('cliente')
			formulario = ClienteActualizarForm(request.POST)
			if formulario.is_valid:
				registro = formulario.save(commit=False)
				historico = ClienteHistorico.objects.get(pk=cliente_id)
				cliente = Cliente.objects.filter(codigo=historico.codigo)[:1].get()

				historico.estado_civil = cliente.estado_civil if registro.estado_civil == '' or registro.estado_civil == None else registro.estado_civil  
				historico.departamento = cliente.departamento if registro.departamento == '' or registro.departamento == None else registro.departamento 
				historico.municipio = cliente.municipio if request.POST.get('municipio') == '' or request.POST.get('municipio_trabajo') == None else Municipio.objects.get(pk=request.POST.get('municipio'))
				historico.colonia = cliente.colonia if registro.colonia == '' or registro.colonia == None else registro.colonia
				historico.referencia = cliente.referencia if registro.referencia == '' or registro.referencia == None else registro.referencia
				historico.telefono_fijo = cliente.telefono_fijo if registro.telefono_fijo == '' or registro.telefono_fijo == None else registro.telefono_fijo
				historico.telefono_celular = cliente.telefono_celular if registro.telefono_celular == '' or registro.telefono_celular == None else registro.telefono_celular
				historico.telefono_celular2 = None if request.POST.get('telefono_celular2') == '' else request.POST.get('telefono_celular2') 
				historico.correo_electronico =  cliente.correo_electronico if registro.correo_electronico == '' or registro.correo_electronico == None else registro.correo_electronico
				historico.profesion_cliente = cliente.profesion_cliente if request.POST.get('profesion_cliente') == '' else Profesion.objects.get(codigo_profesion=request.POST.get('profesion_cliente'))

				historico.ingresos = cliente.ingresos if registro.ingresos == '' else registro.ingresos
				historico.monto_cuentas = cliente.monto_cuentas if registro.monto_cuentas == '' else registro.monto_cuentas 
				historico.departamento_trabajo = cliente.departamento_trabajo if registro.departamento_trabajo == '' or registro.departamento_trabajo == None else registro.departamento_trabajo
				historico.municipio_trabajo = cliente.municipio_trabajo if request.POST.get('municipio_trabajo') == '' or request.POST.get('municipio_trabajo') == None else Municipio.objects.get(pk=request.POST.get('municipio_trabajo'))
				historico.lugar_trabajo = cliente.lugar_trabajo if registro.lugar_trabajo == '' or registro.lugar_trabajo == None else registro.lugar_trabajo
				historico.referencia_trabajo = cliente.referencia_trabajo if registro.referencia_trabajo == '' or registro.referencia_trabajo == None else registro.referencia_trabajo
				historico.telefono_fijo_trabajo = cliente.telefono_fijo_trabajo if registro.telefono_fijo_trabajo == '' or registro.telefono_fijo_trabajo == None else registro.telefono_fijo_trabajo
				historico.correo_electronico_trabajo = cliente.correo_electronico_trabajo if registro.correo_electronico_trabajo == '' or registro.correo_electronico_trabajo == None else registro.correo_electronico_trabajo
				
				historico.tipo_empresa = None if request.POST.get('tipo_empresa') == '' or request.POST.get('tipo_empresa') == None else TipoEmpresa.objects.get(id=request.POST.get('tipo_empresa'))
				historico.actividad_cliente =  cliente.actividad_cliente if request.POST.get('actividad_cliente') == '' or request.POST.get('actividad_cliente') == None else ActividadEconomica.objects.get(codigo_actividad_economica=request.POST.get('actividad_cliente'))
				historico.puesto = None if request.POST.get('puesto') == '' else request.POST.get('puesto')
				historico.antiguedad_anios = None if request.POST.get('antiguedad_anios') == '' else request.POST.get('antiguedad_anios') 
				historico.antiguedad_meses = None if request.POST.get('antiguedad_meses') == '' else request.POST.get('antiguedad_meses') 
				
				historico.actualizado = True
				historico.sucursal = registro.sucursal
				historico.agente = request.user
				historico.filial = registro.filial
				historico.actualizado_por = request.user
				historico.modificado_por = request.user
				
				historico.save()
				fecha = datetime.datetime.today()
				unida = "%s-%s-%s %s" % (fecha.year, fecha.month, fecha.day,  request.POST['hora-inicio']) 

				gestion = Gestion.objects.get(cliente_rechazado=historico)
				gestion.agente = request.user
				gestion.cliente_localizado = historico
				gestion.cliente_rechazado = None
				gestion.telefono = request.POST['telefono']
				gestion.hora_incio = unida
				gestion.tipo_gestion = 1
				gestion.save()


			formulario = ClienteActualizarForm()
			formulario2 = ClienteHistoricoForm()
			clientes = ClienteActualizar.objects.filter(agente=request.user, actualizado=False, codigo_rechazo__isnull= True, gestion__cliente_pendiente__isnull=True).order_by('-fecha_actualizacion')[:5]
			clientes_pendientes = Gestion.objects.filter(cliente_pendiente__isnull=False, agente=request.user).exclude(devolver_llamada__isnull=True).extra({'fecha_cast': "CAST(DevolverLlamada as DATE)"}).order_by('fecha_cast')[:5]
		
			clientes_rechazados = Gestion.objects.filter(cliente_rechazado__isnull=False, agente=request.user).order_by('-hora_final')[:5]
			ctx={
				'formulario': formulario,
				'formulario2': formulario2,
				'clientes': clientes,
				'clientes_pendientes': clientes_pendientes,
				'clientes_rechazados': clientes_rechazados,
				'gestiones': gestiones,
				'recordatorios': recordatorios,
			}
			return render(request, 'actualizar_cliente_callcenter.html', ctx)
		elif request.POST['metodo'] == 'pendiente':
			cliente = ClienteActualizar.objects.get(id=request.POST['cliente'])

			fecha = datetime.datetime.today()
			unida = "%s-%s-%s %s" % (fecha.year, fecha.month, fecha.day,  request.POST['hora-inicio']) 
			
			try:
				gestiones_anteriores = Gestion.objects.filter(cliente_pendiente=cliente)
				gestiones_anteriores.delete() 
			except Exception, e:
				pass

			print fecha

			if request.POST.get('tiempo') == 'pm':
				devolver_llamada = "%s %s%s:00" % (request.POST.get('fecha'), (int(request.POST.get('hora')) + 12), request.POST.get('minuto') )
			else:
				devolver_llamada = "%s %s%s:00" % (request.POST.get('fecha'), request.POST.get('hora'), request.POST.get('minuto') )
			
			date_object = datetime.datetime.strptime(devolver_llamada, '%Y-%m-%d %H:%M:%S')
			

			gestion = Gestion()
			gestion.agente = request.user
			gestion.cliente_pendiente = cliente
			gestion.telefono = request.POST['telefono']
			gestion.hora_incio = unida
			gestion.tipo_gestion = 3
			gestion.identidad = cliente.identidad
			gestion.cliente = cliente.id
			gestion.telefono_contacto = request.POST.get('numero_contacto')
			gestion.nombre_contacto = request.POST.get('nombre_contacto')
			gestion.devolver_llamada = devolver_llamada
			gestion.save()

			clientes = ClienteActualizar.objects.filter(agente=request.user, actualizado=False, codigo_rechazo__isnull= True, gestion__cliente_pendiente__isnull=True).order_by('-fecha_actualizacion')[:5]
			clientes_pendientes = Gestion.objects.filter(cliente_pendiente__isnull=False, agente=request.user).exclude(devolver_llamada__isnull=True).extra({'fecha_cast': "CAST(DevolverLlamada as DATE)"}).order_by('fecha_cast')[:5]
			clientes_rechazados = Gestion.objects.filter(cliente_rechazado__isnull=False, agente=request.user).order_by('-hora_final')[:5]
			
			formulario = ClienteActualizarForm()
			formulario2 = ClienteHistoricoForm()
			ctx={
				'formulario': formulario,
				'formulario2': formulario2,
				'clientes': clientes,
				'clientes_pendientes': clientes_pendientes,
				'clientes_rechazados': clientes_rechazados,
			}
			return render(request, 'actualizar_cliente_callcenter.html', ctx)

def ajax(request):
	if request.is_ajax():
		tabla = request.GET['tabla']
		valor = request.GET['valor']

		if tabla == 'municipio':
			data = list(Municipio.objects.values('id', 'codigo', 'nombre').filter(departamento=valor))
		return HttpResponse(json.dumps(data, default=date_handler), content_type='application/json')

@login_required()
@transaction.atomic
def actualizar_cliente(request):
	if request.is_ajax():
		identidad = request.GET['identidad']
		actualizado = False
		try:
			ClienteHistorico.objects.get(identidad=identidad)
			actualizado = True
			persona = False
		except Exception, e:
			try:
				persona = dict(
					ClienteGeneral.objects.values(
						'id',
						'codigo',
						'primer_nombre',
						'primer_apellido', 
						'segundo_apellido', 
						'sexo', 
						'correo_electronico',
						'telefono_fijo',
						'telefono_celular',
						'identidad',
					).filter(identidad=identidad)[:1].get()
				)
			except Exception, e:
				print e
				persona = False

		data = {
			'actualizado' : actualizado,
			'persona' : persona
		}

		return HttpResponse(json.dumps(data, default=date_handler), content_type='application/json')
	elif request.method == 'GET':
		formulario = ClienteGeneralForm()
		formulario2 = ClienteHistoricoForm()
		ctx={
			'formulario': formulario,
			'formulario2': formulario2,
		}
		return render(request, 'actualizar_cliente.html', ctx)
	elif request.method == 'POST':
		rifa = False
		cliente = ClienteGeneral.objects.get(id=request.POST['id'])
		
		formulario = ClienteGeneralForm(request.POST, instance=cliente)
		formulario2 = ClienteForm(request.POST)
		if formulario.is_valid():
			try:
				try:
					cliente_actualizar = ClienteActualizar.objects.get(identidad=cliente.identidad)
					cliente_actualizar.actualizado = True
					cliente_actualizar.actualizado_por = request.user
					cliente_actualizar.agente = request.user
					cliente_actualizar.save()
				except Exception, e:
					pass

				try:
					gestiones_anteriores = Gestion.objects.filter(cliente_pendiente__identidad=cliente.identidad)
					gestiones_anteriores.delete() 
				except Exception, e:
					pass

				with transaction.atomic():
					cliente = ClienteGeneral.objects.get(id=request.POST['id'])
					cliente.actualizado = True
					cliente.actualizado_por = request.user
					cliente.agente = request.user
					cliente.save()


					actualizar = formulario2.save(commit=False)
					actualizar.identidad = cliente.identidad
					actualizar.primer_nombre = cliente.primer_nombre
					actualizar.primer_apellido = cliente.primer_apellido
					actualizar.segundo_apellido = cliente.segundo_apellido
					actualizar.sexo = cliente.sexo
					actualizar.codigo = cliente.codigo	
					
					actualizar.estado_civil = cliente.estado_civil
					actualizar.departamento = cliente.departamento
					actualizar.municipio = cliente.municipio
					actualizar.colonia = cliente.colonia
					actualizar.referencia = cliente.referencia
					actualizar.telefono_fijo = cliente.telefono_fijo
					actualizar.telefono_celular = cliente.telefono_celular
					actualizar.correo_electronico = cliente.correo_electronico
					actualizar.profesion = cliente.profesion
					actualizar.ingresos = cliente.ingresos
					actualizar.monto_cuentas = cliente.monto_cuentas
					actualizar.departamento_trabajo = cliente.departamento_trabajo
					actualizar.municipio_trabajo = cliente.municipio_trabajo
					actualizar.lugar_trabajo = cliente.lugar_trabajo
					actualizar.referencia_trabajo = cliente.referencia_trabajo
					actualizar.telefono_fijo_trabajo = cliente.telefono_fijo_trabajo
					actualizar.correo_electronico_trabajo = cliente.correo_electronico_trabajo
					actualizar.sucursal = cliente.sucursal
					actualizar.agente = request.user
					actualizar.filial = cliente.filial
					actualizar.actualizado_por = request.user
					actualizar.codigo_rechazo = cliente.codigo_rechazo
					actualizar.comentarios = cliente.comentarios
					actualizar.actualizado = True
					actualizar.codigo = cliente.codigo
					actualizar.con_coopcel = cliente.con_coopcel
					actualizar.actividad_cliente = cliente.actividad_cliente
					actualizar.profesion_cliente = cliente.profesion_cliente
					actualizar.save()

					registro = formulario.save(commit=False)

					historico = ClienteHistorico()
					historico.identidad = registro.identidad
					historico.primer_nombre = registro.primer_nombre
					historico.primer_apellido = registro.primer_apellido
					historico.segundo_apellido = registro.segundo_apellido
					historico.sexo = registro.sexo
					historico.codigo = registro.codigo
					historico.con_coopcel = cliente.con_coopcel
					historico.estado_civil = cliente.estado_civil if registro.estado_civil == '' or registro.estado_civil == None else registro.estado_civil  
					historico.departamento = cliente.departamento if registro.departamento == '' or registro.departamento == None else registro.departamento 
					historico.municipio = cliente.municipio if request.POST.get('municipio') == '' or request.POST.get('municipio_trabajo') == None else Municipio.objects.get(pk=request.POST.get('municipio'))
					historico.colonia = cliente.colonia if registro.colonia == '' or registro.colonia == None else registro.colonia
					historico.referencia = cliente.referencia if registro.referencia == '' or registro.referencia == None else registro.referencia
					historico.telefono_fijo = cliente.telefono_fijo if registro.telefono_fijo == '' or registro.telefono_fijo == None else registro.telefono_fijo
					historico.telefono_celular = cliente.telefono_celular if registro.telefono_celular == '' or registro.telefono_celular == None else registro.telefono_celular
					historico.telefono_celular2 = None if request.POST.get('telefono_celular2') == '' else request.POST.get('telefono_celular2') 
					historico.correo_electronico =  cliente.correo_electronico if registro.correo_electronico == '' or registro.correo_electronico == None else registro.correo_electronico
					historico.profesion_cliente = cliente.profesion_cliente if request.POST.get('profesion_cliente') == '' else Profesion.objects.get(codigo_profesion=request.POST.get('profesion_cliente'))

					historico.ingresos = cliente.ingresos if registro.ingresos == '' else registro.ingresos
					historico.monto_cuentas = cliente.monto_cuentas if registro.monto_cuentas == '' else registro.monto_cuentas 
					historico.departamento_trabajo = cliente.departamento_trabajo if registro.departamento_trabajo == '' or registro.departamento_trabajo == None else registro.departamento_trabajo
					historico.municipio_trabajo = cliente.municipio_trabajo if request.POST.get('municipio_trabajo') == '' or request.POST.get('municipio_trabajo') == None else Municipio.objects.get(pk=request.POST.get('municipio_trabajo'))
					historico.lugar_trabajo = cliente.lugar_trabajo if registro.lugar_trabajo == '' or registro.lugar_trabajo == None else registro.lugar_trabajo
					historico.referencia_trabajo = cliente.referencia_trabajo if registro.referencia_trabajo == '' or registro.referencia_trabajo == None else registro.referencia_trabajo
					historico.telefono_fijo_trabajo = cliente.telefono_fijo_trabajo if registro.telefono_fijo_trabajo == '' or registro.telefono_fijo_trabajo == None else registro.telefono_fijo_trabajo
					historico.correo_electronico_trabajo = cliente.correo_electronico_trabajo if registro.correo_electronico_trabajo == '' or registro.correo_electronico_trabajo == None else registro.correo_electronico_trabajo
					historico.actualizado = True
					historico.sucursal = registro.sucursal
					historico.agente = request.user
					historico.filial = registro.filial
					historico.actualizado_por = request.user
					historico.modificado_por = request.user
					historico.codigo_rechazo = registro.codigo_rechazo
					historico.comentarios = registro.comentarios
					historico.tipo_empresa = None if request.POST.get('tipo_empresa') == '' or request.POST.get('tipo_empresa') == None else TipoEmpresa.objects.get(id=request.POST.get('tipo_empresa'))
					historico.actividad_cliente =  cliente.actividad_cliente if request.POST.get('actividad_cliente') == '' or request.POST.get('actividad_cliente') == None else ActividadEconomica.objects.get(codigo_actividad_economica=request.POST.get('actividad_cliente'))
					historico.puesto = None if request.POST.get('puesto') == '' else request.POST.get('puesto')
					historico.antiguedad_anios = None if request.POST.get('antiguedad_anios') == '' else request.POST.get('antiguedad_anios') 
					historico.antiguedad_meses = None if request.POST.get('antiguedad_meses') == '' else request.POST.get('antiguedad_meses') 
					historico.save()

					with connection.cursor() as cursor:
						cursor.execute("SELECT NEXT VALUE FOR SorteoIdSecuencia AS secuencia;")
						row = cursor.fetchone()
					
					historico.rifa = row[0]
					historico.save()
					
					fecha = datetime.datetime.today()

					gestion = Gestion()
					gestion.agente = request.user
					gestion.cliente_localizado = historico
					gestion.telefono = request.POST['telefono']
					gestion.hora_incio = fecha
					gestion.tipo_gestion = 5
					gestion.identidad = registro.identidad
					gestion.cliente = registro.codigo
					gestion.save()

					rifa = {
						'identidad': historico.identidad,
						'nombres' : "%s %s %s" % (historico.primer_nombre, historico.primer_apellido, historico.segundo_apellido),
						'numero' : historico.rifa
					}

			except Exception, e:
				raise e

			formulario = ClienteActualizarForm()
			formulario2 = ClienteHistoricoForm()
			ctx={
				'formulario': formulario,
				'formulario2': formulario2,
				'rifa' : rifa
			}
			return render(request, 'actualizar_cliente.html', ctx)


#REPORTES
@login_required()
def reporte_clientes(request):
	operadores = User.objects.filter(groups=1)
	if request.method == 'POST':
		query = {}
		query['fecha'] = request.POST['fecha']
		query['cliente_localizado__isnull'] = False
		if  request.POST['operador'] != '':
			query['agente'] = request.POST['operador']

		fecha = request.POST['fecha']
		clientes = Gestion.objects.filter(**query)
	else:
		fecha = ''
		clientes = Gestion.objects.filter(cliente_localizado__isnull=False)

	ctx = {
		'clientes': clientes,
		'fecha': fecha,
		'operadores': operadores,
	}
	return render(request, 'reportes/reporte_clientes.html', ctx)

@login_required()
def reporte_operadores(request):
	if request.method == 'POST':
		fecha = request.POST['fecha']
		clientes = Gestion.objects.values(
			'agente',
			'agente__first_name', 
			'agente__last_name'
		).filter(fecha=fecha).annotate(
			total_localizado=Count('cliente_localizado'), 
			total_no_localizado=Count('cliente_no_localizado'), 
			total=Count('agente')
		)
	else:
		fecha = ''
		clientes = Gestion.objects.values(
			'agente',
			'agente__first_name', 
			'agente__last_name'
		).all().annotate(
			total_localizado=Count('cliente_localizado'), 
			total_no_localizado=Count('cliente_no_localizado'), 
			total=Count('agente')
		)
	print clientes
	ctx = {
		'clientes': clientes,
		'fecha': fecha,
	}
	return render(request, 'reportes/reporte_operadores.html', ctx)

@login_required()
def busqueda_ticket(request):
	if request.is_ajax():
		from django.db.models import Q
		identidad = request.GET.get('identidad')
		try:
			data = dict(ClienteHistorico.objects.values('rifa', 'primer_nombre', 'primer_apellido').filter(Q(identidad=identidad) | Q(codigo=identidad)).order_by('-fecha_actualizacion')[:1].get())
		except Exception as e:
			print e
			data = False
		return HttpResponse(json.dumps(data, default=date_handler), content_type='application/json')
	else:
		return render(request, 'busqueda_ticket.html')

#OTROS DE OPERACIONES
@login_required()
def revision_calidad(request):
	error = False
	exito = False
	operadores = User.objects.filter(groups=1)
	if request.is_ajax():
		codigo_cliente = request.GET['codigo']
		if request.GET.get('metodo') == 'editar':
			exito = False
			if request.GET.get('direccion_residencia') == 'true':
				try:
					cliente = Cliente.objects.filter(codigo=codigo_cliente).order_by('-fecha_actualizacion')[:1].get()
					historico =  ClienteHistorico.objects.filter(codigo=codigo_cliente).order_by('-fecha_actualizacion')[:1].get()

					historico.colonia = None
					historico.referencia = cliente.referencia
					historico.save()
					data ={
						'exito' : 'direccion_residencia',
						'colonia': cliente.colonia,
						'referencia': cliente.referencia,
					}
					print 'PASO POR AQUI'
				except Exception as e:
					data = {}

			if request.GET.get('direccion_trabajo') == 'true':
				try:
					cliente = Cliente.objects.filter(codigo=codigo_cliente).order_by('-fecha_actualizacion')[:1].get()
					historico =  ClienteHistorico.objects.filter(codigo=codigo_cliente).order_by('-fecha_actualizacion')[:1].get()

					historico.referencia_trabajo = cliente.referencia_trabajo
					historico.save()
					data ={
						'exito' : 'direccion_trabajo',
						'referencia_trabajo': cliente.referencia_trabajo
					}
				except Exception as e:
					data = {}

			if request.GET.get('editar') == 'true':
				data = {}
				try:
					historico =  ClienteHistorico.objects.filter(codigo=codigo_cliente).order_by('-fecha_actualizacion')[:1].get()
					historico.colonia = request.GET.get('colonia')
					historico.referencia = request.GET.get('referencia')
					historico.referencia_trabajo = request.GET.get('referencia_trabajo')
					historico.correo_electronico = request.GET.get('correo_electronico')
					historico.telefono_fijo = request.GET.get('telefono_fijo')
					historico.telefono_celular = request.GET.get('telefono_celular')
					historico.lugar_trabajo = request.GET.get('lugar_trabajo')
					historico.referencia_trabajo = request.GET.get('referencia_trabajo')
					historico.telefono_fijo_trabajo = request.GET.get('telefono_fijo_trabajo')
					historico.correo_electronico_trabajo = request.GET.get('correo_electronico_trabajo')
					historico.puesto = request.GET.get('puesto')

					historico.save()
					data ={
						'editar' : True,
						'colonia': historico.colonia,
						'referencia': historico.referencia,
						'referencia_trabajo': historico.referencia_trabajo,
						'correo_electronico': historico.correo_electronico,
						'telefono_fijo': historico.telefono_fijo,
						'telefono_celular': historico.telefono_celular,
						'lugar_trabajo': historico.lugar_trabajo,
						'referencia_trabajo': historico.referencia_trabajo,
						'telefono_fijo_trabajo': historico.telefono_fijo_trabajo,
						'correo_electronico_trabajo': historico.correo_electronico_trabajo,
						'puesto': historico.puesto,
					

					}
				except Exception as e:
					print e

			print request.GET.get('editar'), request.GET.get('direccion_trabajo'),request.GET.get('direccion_residencia'), request.GET.get('codigo'), request.GET.get('telefono_fijo_trabajo')

		else:
			try:
				cliente = dict(
					Cliente.objects.values(
						'id',
						'codigo',
						'identidad',
						'primer_nombre',
						'segundo_apellido',
						'primer_apellido',
						'sexo',
						'estado_civil',
						'departamento__nombre',
						'municipio__nombre',
						'colonia',
						'referencia',
						'telefono_fijo',
						'telefono_celular',
						'correo_electronico',
						'profesion',
						'ingresos',
						'monto_cuentas',
						'departamento_trabajo__nombre',
						'municipio_trabajo__nombre',
						'lugar_trabajo',
						'referencia_trabajo',
						'telefono_fijo_trabajo',
						'correo_electronico_trabajo',
						'actualizado',
						'sucursal',
						'agente',
						'filial__nombre',
						'actualizado_por',
						'fecha_actualizacion',
						'codigo_rechazo',
						'comentarios',
						'profesion_cliente__descripcion',
						'actividad_cliente__descripcion'
					).filter(codigo=codigo_cliente).order_by('-fecha_actualizacion')[:1].get()
				)


				historico = dict(
					ClienteHistorico.objects.values(
						'id',
						'codigo',
						'identidad',
						'primer_nombre',
						'segundo_apellido',
						'primer_apellido',
						'sexo',
						'estado_civil',
						'departamento__nombre',
						'municipio__nombre',
						'colonia',
						'referencia',
						'telefono_fijo',
						'telefono_celular',
						'correo_electronico',
						'profesion',
						'ingresos',
						'monto_cuentas',
						'departamento_trabajo__nombre',
						'municipio_trabajo__nombre',
						'lugar_trabajo',
						'referencia_trabajo',
						'telefono_fijo_trabajo',
						'correo_electronico_trabajo',
						'actualizado',
						'sucursal',
						'agente__first_name',
						'agente__last_name',
						'filial__nombre',
						'actualizado_por',
						'fecha_actualizacion',
						'codigo_rechazo',
						'comentarios',
						'puesto',
						'profesion_cliente__descripcion',
						'actividad_cliente__descripcion',
						'rifa'
					).filter(codigo=codigo_cliente).order_by('-fecha_actualizacion')[:1].get()
				)
			except Exception, e:
				raise e
				cliente = False
				historico = False

			data = {
				'cliente': cliente,
				'historico':historico,
			}

		return HttpResponse(json.dumps(data, default=date_handler), content_type='application/json')
	elif request.method == 'POST':
		query = {}
		fecha = '' if request.POST.get('fecha') == '' else request.POST.get('fecha')
		if fecha != None and fecha !='':
			query['fecha'] = fecha
		query['cliente_localizado__isnull'] = False
		clientes = Gestion.objects.filter(**query).exclude(cliente_localizado__actualizado_core=True)[:15]
		if request.POST['metodo'] == 'migracion':
			from django.db import connection, transaction
			cursor = connection.cursor()
			try:
				query = "EXEC dbo.ActualizaCliente @ClienteId=%s , @Id=0"%request.POST['codigo_cliente'] 
				cursor.execute(query)
				row = cursor.fetchall()
				transaction.commit()
				exito = True
			except Exception as e:
				error = True
			finally:
				cursor.close()

		elif request.POST['metodo'] == 'rechazar':
			cliente = ClienteHistorico.objects.get(pk=request.POST['cliente_historico'])
			gestion = Gestion.objects.get(pk=request.POST['gestion'])
			gestion.cliente_localizado = None
			gestion.cliente_rechazado = cliente
			gestion.tipo_gestion = 5
			gestion.save()
			exito = True
	else:
		fecha = ''
		clientes = Gestion.objects.filter(cliente_localizado__isnull=False).exclude(cliente_localizado__actualizado_core=True)[:15]

	ctx = {
		'clientes': clientes,
		'fecha': fecha,
		'operadores': operadores,
		'error':error,
		'exito':exito,
	}
	return render(request, 'revision_calidad.html', ctx)

@login_required()
def modificar_cliente(request):
	if request.is_ajax():
		identidad = request.GET['identidad']
		actualizado = False
		try:
			persona = dict(
				ClienteHistorico.objects.values(
					'id',
					'codigo',
					'identidad',
					'primer_nombre',
					'primer_apellido',
					'segundo_apellido',
					'sexo',
					'estado_civil',
					'departamento',
					'municipio',
					'colonia',
					'referencia',
					'telefono_fijo',
					'telefono_celular',
					'correo_electronico',
					'profesion',
					'ingresos',
					'monto_cuentas',
					'departamento_trabajo',
					'municipio_trabajo',
					'lugar_trabajo',
					'referencia_trabajo',
					'telefono_fijo_trabajo',
					'correo_electronico_trabajo',
					'actualizado',
					'sucursal',
					'agente',
					'filial',
					'actualizado_por',
					'fecha_actualizacion',
					'codigo_rechazo',
					'comentarios',
					'telefono_celular2',
					'tipo_empresa',
					'puesto',
					'antiguedad_anios',
					'antiguedad_meses',
					'rifa',
					'profesion_cliente',
					'actividad_cliente',
					'actualizado_core',
					'con_coopcel',
				).filter(identidad=identidad).order_by('-fecha_actualizacion')[:1].get()
			)
		except Exception, e:
			print e
			persona = False

		data = {
			'actualizado' : actualizado,
			'persona' : persona
		}

		return HttpResponse(json.dumps(data, default=date_handler), content_type='application/json')
	elif request.method == 'GET':
		formulario = ClienteGeneralForm()
		formulario2 = ClienteHistoricoForm()
		ctx={
			'formulario': formulario,
			'formulario2': formulario2,
		}
		return render(request, 'modificar_cliente.html', ctx)
	elif request.method == 'POST':
		historico = ClienteHistorico.objects.get(id=request.POST['id'])
		print historico
		formulario = ClienteActualizarForm(request.POST)
		if formulario.is_valid:
			registro = formulario.save(commit=False)
			cliente = Cliente.objects.filter(codigo=historico.codigo)[:1].get()

			historico.estado_civil = cliente.estado_civil if registro.estado_civil == '' or registro.estado_civil == None else registro.estado_civil  
			historico.departamento = cliente.departamento if registro.departamento == '' or registro.departamento == None else registro.departamento 
			historico.municipio = cliente.municipio if request.POST.get('municipio') == '' or request.POST.get('municipio_trabajo') == None else Municipio.objects.get(pk=request.POST.get('municipio'))
			historico.colonia = cliente.colonia if registro.colonia == '' or registro.colonia == None else registro.colonia
			historico.referencia = cliente.referencia if registro.referencia == '' or registro.referencia == None else registro.referencia
			historico.telefono_fijo = cliente.telefono_fijo if registro.telefono_fijo == '' or registro.telefono_fijo == None else registro.telefono_fijo
			historico.telefono_celular = cliente.telefono_celular if registro.telefono_celular == '' or registro.telefono_celular == None else registro.telefono_celular
			historico.telefono_celular2 = None if request.POST.get('telefono_celular2') == '' else request.POST.get('telefono_celular2') 
			historico.correo_electronico =  cliente.correo_electronico if registro.correo_electronico == '' or registro.correo_electronico == None else registro.correo_electronico
			historico.profesion_cliente = cliente.profesion_cliente if request.POST.get('profesion_cliente') == '' else Profesion.objects.get(codigo_profesion=request.POST.get('profesion_cliente'))

			historico.ingresos = cliente.ingresos if registro.ingresos == '' else registro.ingresos
			historico.monto_cuentas = cliente.monto_cuentas if registro.monto_cuentas == '' else registro.monto_cuentas 
			historico.departamento_trabajo = cliente.departamento_trabajo if registro.departamento_trabajo == '' or registro.departamento_trabajo == None else registro.departamento_trabajo
			historico.municipio_trabajo = cliente.municipio_trabajo if request.POST.get('municipio_trabajo') == '' or request.POST.get('municipio_trabajo') == None else Municipio.objects.get(pk=request.POST.get('municipio_trabajo'))
			historico.lugar_trabajo = cliente.lugar_trabajo if registro.lugar_trabajo == '' or registro.lugar_trabajo == None else registro.lugar_trabajo
			historico.referencia_trabajo = cliente.referencia_trabajo if registro.referencia_trabajo == '' or registro.referencia_trabajo == None else registro.referencia_trabajo
			historico.telefono_fijo_trabajo = cliente.telefono_fijo_trabajo if registro.telefono_fijo_trabajo == '' or registro.telefono_fijo_trabajo == None else registro.telefono_fijo_trabajo
			historico.correo_electronico_trabajo = cliente.correo_electronico_trabajo if registro.correo_electronico_trabajo == '' or registro.correo_electronico_trabajo == None else registro.correo_electronico_trabajo
			
			historico.tipo_empresa = None if request.POST.get('tipo_empresa') == '' or request.POST.get('tipo_empresa') == None else TipoEmpresa.objects.get(id=request.POST.get('tipo_empresa'))
			historico.actividad_cliente =  cliente.actividad_cliente if request.POST.get('actividad_cliente') == '' or request.POST.get('actividad_cliente') == None else ActividadEconomica.objects.get(codigo_actividad_economica=request.POST.get('actividad_cliente'))
			historico.puesto = None if request.POST.get('puesto') == '' else request.POST.get('puesto')
			historico.antiguedad_anios = None if request.POST.get('antiguedad_anios') == '' else request.POST.get('antiguedad_anios') 
			historico.antiguedad_meses = None if request.POST.get('antiguedad_meses') == '' else request.POST.get('antiguedad_meses') 
			
			historico.sucursal = registro.sucursal
			historico.filial = registro.filial
			historico.modificado_por = request.user
			
			historico.save()

			formulario = ClienteActualizarForm()
			formulario2 = ClienteHistoricoForm()
			ctx={
				'formulario': formulario,
				'formulario2': formulario2,
			}
			return render(request, 'modificar_cliente.html', ctx)



#COBRANZAS
@login_required()
@transaction.atomic
def prestamos_fiduciarios(request):
	gest= Gestion.objects.filter(cliente_pendiente__isnull=False, devolver_llamada__isnull=False, agente=request.user)
	recordatorios = []
	for gestion in gest:
		fecha = datetime.datetime.today()
		date_object = datetime.datetime.strptime(gestion.devolver_llamada+'.000000', '%Y-%m-%d %H:%M:%S.%f')
		if fecha >= date_object:
			recordatorios.append({'cliente': gestion.cliente_pendiente.primer_nombre+ ' ' + gestion.cliente_pendiente.primer_apellido , 'fecha': date_object.strftime('%Y-%m-%d %I:%M:%S%p')})

	gestiones = Gestion.objects.values(
		'agente',
		'agente__first_name', 
		'agente__last_name'
	).filter(fecha= datetime.date.today(), agente=request.user).annotate(
		total_localizado=Count('cliente_localizado'), 
		total_no_localizado=Count('cliente_no_localizado'), 
		total_pendiente=Count('cliente_pendiente'), 
		total=Count('agente')
	)
	if request.is_ajax():
		id = request.GET['id']
		try:
			if request.GET.get('metodo') != '' and request.GET.get('metodo') != None:
				persona = dict(
					ClienteHistorico.objects.values(
						'id',
						'codigo',
						'identidad',
						'primer_nombre',
						'primer_apellido',
						'segundo_apellido',
						'sexo',
						'estado_civil',
						'departamento',
						'municipio',
						'colonia',
						'referencia',
						'telefono_fijo',
						'telefono_celular',
						'correo_electronico',
						'profesion',
						'ingresos',
						'monto_cuentas',
						'departamento_trabajo',
						'municipio_trabajo',
						'lugar_trabajo',
						'referencia_trabajo',
						'telefono_fijo_trabajo',
						'correo_electronico_trabajo',
						'actualizado',
						'sucursal',
						'agente',
						'filial',
						'actualizado_por',
						'fecha_actualizacion',
						'codigo_rechazo',
						'comentarios',
						'telefono_celular2',
						'tipo_empresa',
						'puesto',
						'antiguedad_anios',
						'antiguedad_meses',
						'rifa',
						'profesion_cliente',
						'actividad_cliente',
						'actualizado_core',
						'con_coopcel',
					).get(id=id)
				)
			else:
				persona = dict(
					ClienteActualizar.objects.values(
						'codigo',
						'primer_nombre',
						'primer_apellido', 
						'segundo_apellido', 
						'sexo', 
						'correo_electronico',
						'telefono_fijo',
						'telefono_celular',
						'identidad',
						'con_coopcel'
					).get(id=id)
				)
			gestiones = list(
				Gestion.objects.values(
					'agente__first_name',
					'agente__last_name',
					'fecha',
					'hora_incio',
					'telefono',
					'tipo_gestion'
				).filter(cliente=persona['codigo'])
			)
			print gestiones
		except Exception, e:
			print e
			persona = False
			gestiones = False

		data = {
			'gestiones': gestiones,
			'persona': persona
		}

		return HttpResponse(json.dumps(data, default=date_handler), content_type='application/json')
	elif request.method == 'GET':
		clientes = ClienteActualizar.objects.filter(agente=request.user, actualizado=False, codigo_rechazo__isnull= True, gestion__cliente_pendiente__isnull=True).order_by('-primer_apellido')[:5]
		clientes_pendientes = Gestion.objects.filter(cliente_pendiente__isnull=False, agente=request.user).exclude(devolver_llamada__isnull=True).extra({'fecha_cast': "CAST(DevolverLlamada as DATE)"}).order_by('fecha_cast')[:5]
		clientes_rechazados = Gestion.objects.filter(cliente_rechazado__isnull=False, agente=request.user).order_by('-hora_final')[:5]
		
		formulario = ClienteActualizarForm()
		formulario2 = ClienteHistoricoForm()
		ctx={
			'formulario': formulario,
			'formulario2': formulario2,
			'clientes': clientes,
			'clientes_pendientes': clientes_pendientes,
			'clientes_rechazados': clientes_rechazados,
			'gestiones': gestiones,
			'recordatorios': recordatorios,
		}
		return render(request, 'prospectacion/prestamos_fiduciarios.html', ctx)
	elif request.method == 'POST':
		rifa = False
		if request.POST['metodo'] == 'actualizar':
			cliente = ClienteActualizar.objects.get(id=request.POST['modal-localizado-cliente'])
			if int(request.POST['tipo-gestion']) == 3:
				fecha = datetime.datetime.today()
				unida = "%s-%s-%s %s" % (fecha.year, fecha.month, fecha.day,  request.POST['hora-inicio']) 
				
				try:
					gestiones_anteriores = Gestion.objects.filter(cliente_pendiente=cliente)
					gestiones_anteriores.delete() 
				except Exception, e:
					pass

				gestion = Gestion()
				gestion.agente = request.user
				gestion.cliente_pendiente = cliente
				gestion.telefono = request.POST['telefono']
				gestion.hora_incio = unida
				gestion.tipo_gestion = 3
				gestion.identidad = cliente.identidad
				gestion.cliente = cliente.id
				gestion.save()
			elif int(request.POST['tipo-gestion']) == 4:
				cliente = ClienteActualizar.objects.get(id=request.POST['modal-localizado-cliente'])
				try:
					gestiones_anteriores = Gestion.objects.filter(cliente_pendiente=cliente)
					gestiones_anteriores.delete() 
				except Exception, e:
					pass

				try:
					with transaction.atomic():
						cliente.actualizado_por = request.user
						cliente.actualizado = True
						cliente.agente = request.user
						cliente.save()


						actualizar = Cliente()
						actualizar.identidad = cliente.identidad
						actualizar.primer_nombre = cliente.primer_nombre
						actualizar.primer_apellido = cliente.primer_apellido
						actualizar.segundo_apellido = cliente.segundo_apellido
						actualizar.sexo = cliente.sexo
					
						actualizar.estado_civil = cliente.estado_civil
						actualizar.codigo = cliente.id
						actualizar.departamento = cliente.departamento
						actualizar.municipio = cliente.municipio
						actualizar.colonia = cliente.colonia
						actualizar.referencia = cliente.referencia
						actualizar.telefono_fijo = cliente.telefono_fijo
						actualizar.telefono_celular = cliente.telefono_celular
						actualizar.correo_electronico = cliente.correo_electronico
						actualizar.profesion = cliente.profesion
						actualizar.ingresos = cliente.ingresos
						actualizar.monto_cuentas = cliente.monto_cuentas
						actualizar.departamento_trabajo = cliente.departamento_trabajo
						actualizar.municipio_trabajo = cliente.municipio_trabajo
						actualizar.lugar_trabajo = cliente.lugar_trabajo
						actualizar.referencia_trabajo = cliente.referencia_trabajo
						actualizar.telefono_fijo_trabajo = cliente.telefono_fijo_trabajo
						actualizar.correo_electronico_trabajo = cliente.correo_electronico_trabajo
						actualizar.actualizado_por = request.user
						actualizar.con_coopcel = cliente.con_coopcel
						actualizar.actividad_cliente = cliente.actividad_cliente
						actualizar.profesion_cliente = cliente.profesion_cliente
						actualizar.agente = request.user
						actualizar.save()
						

						fecha = datetime.date.today()
						unida = "%s-%s-%s %s" % (fecha.year, fecha.month, fecha.day,  request.POST['hora-inicio']) 
						gestion = Gestion()
						gestion.agente = request.user
						gestion.cliente_no_localizado = actualizar
						gestion.telefono = request.POST['telefono']
						gestion.hora_incio = timezone.now()
						gestion.tipo_gestion = 4
						gestion.identidad = cliente.identidad
						gestion.cliente = cliente.id
						gestion.save()

				except Exception, e:
					print e
					pass
			else:
				formulario = ClienteActualizarForm(request.POST, instance=cliente)
				formulario2 = ClienteForm(request.POST)
				if formulario.is_valid():
					try:
						try:
							gestiones_anteriores = Gestion.objects.filter(cliente_pendiente=cliente)
							gestiones_anteriores.delete() 
						except Exception, e:
							pass

						with transaction.atomic():
							try:
								cliente_actualizar = ClienteGeneral.objects.get(identidad=cliente.identidad)
								cliente_actualizar.actualizado = True
								cliente_actualizar.actualizado_por = request.user
								cliente_actualizar.agente = request.user
								cliente_actualizar.save()
							except Exception, e:
								pass
								
							cliente = ClienteActualizar.objects.get(id=request.POST['modal-localizado-cliente'])
							cliente.actualizado = True
							cliente.actualizado_por = request.user
							cliente.agente = request.user
							cliente.save()


							actualizar = formulario2.save(commit=False)
							actualizar.identidad = cliente.identidad
							actualizar.primer_nombre = cliente.primer_nombre
							actualizar.primer_apellido = cliente.primer_apellido
							actualizar.segundo_apellido = cliente.segundo_apellido
							actualizar.sexo = cliente.sexo
							actualizar.codigo = cliente.codigo	
						
							actualizar.estado_civil = cliente.estado_civil
							actualizar.departamento = cliente.departamento
							actualizar.municipio = cliente.municipio
							actualizar.colonia = cliente.colonia
							actualizar.referencia = cliente.referencia
							actualizar.telefono_fijo = cliente.telefono_fijo
							actualizar.telefono_celular = cliente.telefono_celular
							actualizar.correo_electronico = cliente.correo_electronico
							actualizar.profesion = cliente.profesion
							actualizar.ingresos = cliente.ingresos
							actualizar.monto_cuentas = cliente.monto_cuentas
							actualizar.departamento_trabajo = cliente.departamento_trabajo
							actualizar.municipio_trabajo = cliente.municipio_trabajo
							actualizar.lugar_trabajo = cliente.lugar_trabajo
							actualizar.referencia_trabajo = cliente.referencia_trabajo
							actualizar.telefono_fijo_trabajo = cliente.telefono_fijo_trabajo
							actualizar.correo_electronico_trabajo = cliente.correo_electronico_trabajo
							actualizar.sucursal = cliente.sucursal
							actualizar.agente = request.user
							actualizar.filial = cliente.filial
							actualizar.actualizado_por = request.user
							actualizar.codigo_rechazo = cliente.codigo_rechazo
							actualizar.comentarios = cliente.comentarios
							actualizar.actualizado = True
							actualizar.codigo = cliente.codigo
							actualizar.con_coopcel = cliente.con_coopcel
							actualizar.actividad_cliente = cliente.actividad_cliente
							actualizar.profesion_cliente = cliente.profesion_cliente
							actualizar.save()


							registro = formulario.save(commit=False)
							historico = ClienteHistorico()
						
							historico.identidad = registro.identidad
							historico.primer_nombre = registro.primer_nombre
							historico.primer_apellido = registro.primer_apellido
							historico.segundo_apellido = registro.segundo_apellido
							historico.sexo = registro.sexo
							historico.codigo = registro.codigo

							historico.estado_civil = cliente.estado_civil if registro.estado_civil == '' or registro.estado_civil == None else registro.estado_civil  
							historico.departamento = cliente.departamento if registro.departamento == '' or registro.departamento == None else registro.departamento 
							historico.municipio = cliente.municipio if request.POST.get('municipio') == '' or request.POST.get('municipio_trabajo') == None else Municipio.objects.get(pk=request.POST.get('municipio'))
							historico.colonia = cliente.colonia if registro.colonia == '' or registro.colonia == None else registro.colonia
							historico.referencia = cliente.referencia if registro.referencia == '' or registro.referencia == None else registro.referencia
							historico.telefono_fijo = cliente.telefono_fijo if registro.telefono_fijo == '' or registro.telefono_fijo == None else registro.telefono_fijo
							historico.telefono_celular = cliente.telefono_celular if registro.telefono_celular == '' or registro.telefono_celular == None else registro.telefono_celular
							historico.telefono_celular2 = None if request.POST.get('telefono_celular2') == '' else request.POST.get('telefono_celular2') 
							historico.correo_electronico =  cliente.correo_electronico if registro.correo_electronico == '' or registro.correo_electronico == None else registro.correo_electronico
							historico.profesion_cliente = cliente.profesion_cliente if request.POST.get('profesion_cliente') == '' else Profesion.objects.get(codigo_profesion=request.POST.get('profesion_cliente'))

							historico.ingresos = cliente.ingresos if registro.ingresos == '' else registro.ingresos
							historico.monto_cuentas = cliente.monto_cuentas if registro.monto_cuentas == '' else registro.monto_cuentas 
							historico.departamento_trabajo = cliente.departamento_trabajo if registro.departamento_trabajo == '' or registro.departamento_trabajo == None else registro.departamento_trabajo
							historico.municipio_trabajo = cliente.municipio_trabajo if request.POST.get('municipio_trabajo') == '' or request.POST.get('municipio_trabajo') == None else Municipio.objects.get(pk=request.POST.get('municipio_trabajo'))
							historico.lugar_trabajo = cliente.lugar_trabajo if registro.lugar_trabajo == '' or registro.lugar_trabajo == None else registro.lugar_trabajo
							historico.referencia_trabajo = cliente.referencia_trabajo if registro.referencia_trabajo == '' or registro.referencia_trabajo == None else registro.referencia_trabajo
							historico.telefono_fijo_trabajo = cliente.telefono_fijo_trabajo if registro.telefono_fijo_trabajo == '' or registro.telefono_fijo_trabajo == None else registro.telefono_fijo_trabajo
							historico.correo_electronico_trabajo = cliente.correo_electronico_trabajo if registro.correo_electronico_trabajo == '' or registro.correo_electronico_trabajo == None else registro.correo_electronico_trabajo
							
							historico.tipo_empresa = None if request.POST.get('tipo_empresa') == '' or request.POST.get('tipo_empresa') == None else TipoEmpresa.objects.get(id=request.POST.get('tipo_empresa'))
							historico.actividad_cliente =  cliente.actividad_cliente if request.POST.get('actividad_cliente') == '' or request.POST.get('actividad_cliente') == None else ActividadEconomica.objects.get(codigo_actividad_economica=request.POST.get('actividad_cliente'))
							historico.puesto = None if request.POST.get('puesto') == '' else request.POST.get('puesto')
							historico.antiguedad_anios = None if request.POST.get('antiguedad_anios') == '' else request.POST.get('antiguedad_anios') 
							historico.antiguedad_meses = None if request.POST.get('antiguedad_meses') == '' else request.POST.get('antiguedad_meses') 
							
							historico.actualizado = True
							historico.sucursal = registro.sucursal
							historico.agente = request.user
							historico.filial = registro.filial
							historico.actualizado_por = request.user
							historico.modificado_por = request.user
							historico.codigo_rechazo = registro.codigo_rechazo
							historico.con_coopcel = cliente.con_coopcel
							historico.comentarios = registro.comentarios

							historico.save()

							with connection.cursor() as cursor:
								cursor.execute("SELECT NEXT VALUE FOR SorteoIdSecuencia AS secuencia;")
								row = cursor.fetchone()
							
							historico.rifa = row[0]
							historico.save()
							
							print row
							fecha = datetime.datetime.today()
							unida = "%s-%s-%s %s" % (fecha.year, fecha.month, fecha.day,  request.POST['hora-inicio']) 

							gestion = Gestion()
							gestion.agente = request.user
							gestion.cliente_localizado = historico
							gestion.telefono = request.POST['telefono']
							gestion.hora_incio = unida
							gestion.tipo_gestion = 1
							gestion.identidad = registro.identidad
							gestion.cliente = registro.codigo
							gestion.save()

							rifa = {
								'identidad': historico.identidad,
								'nombres' : "%s %s %s" % (historico.primer_nombre, historico.primer_apellido, historico.segundo_apellido),
								'numero' : historico.rifa
							}

					except Exception, e:
						raise e
				else:
					print formulario.errors

			formulario = ClienteActualizarForm()
			formulario2 = ClienteHistoricoForm()
			clientes = ClienteActualizar.objects.filter(agente=request.user, actualizado=False, codigo_rechazo__isnull= True, gestion__cliente_pendiente__isnull=True).order_by('-fecha_actualizacion')[:5]
			clientes_pendientes = Gestion.objects.filter(cliente_pendiente__isnull=False, agente=request.user).exclude(devolver_llamada__isnull=True).extra({'fecha_cast': "CAST(DevolverLlamada as DATE)"}).order_by('fecha_cast')[:5]
			clientes_rechazados = Gestion.objects.filter(cliente_rechazado__isnull=False, agente=request.user).order_by('-hora_final')[:5]
			ctx={
				'formulario': formulario,
				'formulario2': formulario2,
				'clientes': clientes,
				'clientes_pendientes': clientes_pendientes,
				'clientes_rechazados': clientes_rechazados,
				'gestiones': gestiones,
				'recordatorios': recordatorios,
				'rifa' : rifa
			}
			return render(request, 'prospectacion/prestamos_fiduciarios.html', ctx)
		elif request.POST['metodo'] == 'no-localizado':
			cliente = ClienteActualizar.objects.get(id=request.POST['modal-no-localizado-cliente'])
			try:
				try:
					gestiones_anteriores = Gestion.objects.filter(cliente_pendiente=cliente)
					gestiones_anteriores.delete() 
				except Exception, e:
					pass

				with transaction.atomic():
					cliente.codigo_rechazo = request.POST['razon']
					cliente.comentarios = request.POST['comentarios']
					cliente.codigo = cliente.id
					cliente.actualizado_por = request.user
					cliente.agente = request.user
					cliente.save()

					actualizar = Cliente()
					actualizar.identidad = cliente.identidad
					actualizar.primer_nombre = cliente.primer_nombre
					actualizar.primer_apellido = cliente.primer_apellido
					actualizar.segundo_apellido = cliente.segundo_apellido
					actualizar.sexo = cliente.sexo
					actualizar.codigo = cliente.id
				
					actualizar.estado_civil = cliente.estado_civil
					actualizar.departamento = cliente.departamento
					actualizar.municipio = cliente.municipio
					actualizar.colonia = cliente.colonia
					actualizar.referencia = cliente.referencia
					actualizar.telefono_fijo = cliente.telefono_fijo
					actualizar.telefono_celular = cliente.telefono_celular
					actualizar.correo_electronico = cliente.correo_electronico
					actualizar.profesion = cliente.profesion

					actualizar.ingresos = cliente.ingresos

					actualizar.monto_cuentas = cliente.monto_cuentas
					actualizar.departamento_trabajo = cliente.departamento_trabajo
					actualizar.municipio_trabajo = cliente.municipio_trabajo
					actualizar.lugar_trabajo = cliente.lugar_trabajo
					actualizar.referencia_trabajo = cliente.referencia_trabajo
					actualizar.telefono_fijo_trabajo = cliente.telefono_fijo_trabajo
					actualizar.correo_electronico_trabajo = cliente.correo_electronico_trabajo	
					actualizar.codigo_rechazo = request.POST['razon']
					actualizar.comentarios = request.POST['comentarios']
					actualizar.actualizado_por = request.user
					actualizar.agente = request.user
					actualizar.con_coopcel = cliente.con_coopcel

					actualizar.actividad_cliente = cliente.actividad_cliente
					actualizar.profesion_cliente = cliente.profesion_cliente
					actualizar.save()
					
					fecha = datetime.datetime.today()
					unida = "%s-%s-%s %s" % (fecha.year, fecha.month, fecha.day,  request.POST['hora-inicio']) 

					gestion = Gestion()
					gestion.agente = request.user
					gestion.cliente_no_localizado = actualizar
					gestion.telefono = request.POST['telefono']
					gestion.hora_incio = unida
					gestion.tipo_gestion = 2
					gestion.identidad = cliente.identidad
					gestion.cliente = cliente.id
					gestion.save()

			except Exception, e:
				pass


			formulario = ClienteActualizarForm()
			formulario2 = ClienteHistoricoForm()
			clientes = ClienteActualizar.objects.filter(agente=request.user, actualizado=False, codigo_rechazo__isnull= True, gestion__cliente_pendiente__isnull=True).order_by('-fecha_actualizacion')[:5]
			clientes_pendientes = Gestion.objects.filter(cliente_pendiente__isnull=False, agente=request.user).exclude(devolver_llamada__isnull=True).extra({'fecha_cast': "CAST(DevolverLlamada as DATE)"}).order_by('fecha_cast')[:5]
		
			clientes_rechazados = Gestion.objects.filter(cliente_rechazado__isnull=False, agente=request.user).order_by('-hora_final')[:5]
			ctx={
				'formulario': formulario,
				'formulario2': formulario2,
				'clientes': clientes,
				'clientes_pendientes': clientes_pendientes,
				'clientes_rechazados': clientes_rechazados,
				'gestiones': gestiones,
				'recordatorios': recordatorios,
			}
			return render(request, 'prospectacion/prestamos_fiduciarios.html', ctx)		
		elif request.POST['metodo'] == 'rechazado':
			cliente_id = request.POST.get('cliente')
			formulario = ClienteActualizarForm(request.POST)
			if formulario.is_valid:
				registro = formulario.save(commit=False)
				historico = ClienteHistorico.objects.get(pk=cliente_id)
				cliente = Cliente.objects.filter(codigo=historico.codigo)[:1].get()

				historico.estado_civil = cliente.estado_civil if registro.estado_civil == '' or registro.estado_civil == None else registro.estado_civil  
				historico.departamento = cliente.departamento if registro.departamento == '' or registro.departamento == None else registro.departamento 
				historico.municipio = cliente.municipio if request.POST.get('municipio') == '' or request.POST.get('municipio_trabajo') == None else Municipio.objects.get(pk=request.POST.get('municipio'))
				historico.colonia = cliente.colonia if registro.colonia == '' or registro.colonia == None else registro.colonia
				historico.referencia = cliente.referencia if registro.referencia == '' or registro.referencia == None else registro.referencia
				historico.telefono_fijo = cliente.telefono_fijo if registro.telefono_fijo == '' or registro.telefono_fijo == None else registro.telefono_fijo
				historico.telefono_celular = cliente.telefono_celular if registro.telefono_celular == '' or registro.telefono_celular == None else registro.telefono_celular
				historico.telefono_celular2 = None if request.POST.get('telefono_celular2') == '' else request.POST.get('telefono_celular2') 
				historico.correo_electronico =  cliente.correo_electronico if registro.correo_electronico == '' or registro.correo_electronico == None else registro.correo_electronico
				historico.profesion_cliente = cliente.profesion_cliente if request.POST.get('profesion_cliente') == '' else Profesion.objects.get(codigo_profesion=request.POST.get('profesion_cliente'))

				historico.ingresos = cliente.ingresos if registro.ingresos == '' else registro.ingresos
				historico.monto_cuentas = cliente.monto_cuentas if registro.monto_cuentas == '' else registro.monto_cuentas 
				historico.departamento_trabajo = cliente.departamento_trabajo if registro.departamento_trabajo == '' or registro.departamento_trabajo == None else registro.departamento_trabajo
				historico.municipio_trabajo = cliente.municipio_trabajo if request.POST.get('municipio_trabajo') == '' or request.POST.get('municipio_trabajo') == None else Municipio.objects.get(pk=request.POST.get('municipio_trabajo'))
				historico.lugar_trabajo = cliente.lugar_trabajo if registro.lugar_trabajo == '' or registro.lugar_trabajo == None else registro.lugar_trabajo
				historico.referencia_trabajo = cliente.referencia_trabajo if registro.referencia_trabajo == '' or registro.referencia_trabajo == None else registro.referencia_trabajo
				historico.telefono_fijo_trabajo = cliente.telefono_fijo_trabajo if registro.telefono_fijo_trabajo == '' or registro.telefono_fijo_trabajo == None else registro.telefono_fijo_trabajo
				historico.correo_electronico_trabajo = cliente.correo_electronico_trabajo if registro.correo_electronico_trabajo == '' or registro.correo_electronico_trabajo == None else registro.correo_electronico_trabajo
				
				historico.tipo_empresa = None if request.POST.get('tipo_empresa') == '' or request.POST.get('tipo_empresa') == None else TipoEmpresa.objects.get(id=request.POST.get('tipo_empresa'))
				historico.actividad_cliente =  cliente.actividad_cliente if request.POST.get('actividad_cliente') == '' or request.POST.get('actividad_cliente') == None else ActividadEconomica.objects.get(codigo_actividad_economica=request.POST.get('actividad_cliente'))
				historico.puesto = None if request.POST.get('puesto') == '' else request.POST.get('puesto')
				historico.antiguedad_anios = None if request.POST.get('antiguedad_anios') == '' else request.POST.get('antiguedad_anios') 
				historico.antiguedad_meses = None if request.POST.get('antiguedad_meses') == '' else request.POST.get('antiguedad_meses') 
				
				historico.actualizado = True
				historico.sucursal = registro.sucursal
				historico.agente = request.user
				historico.filial = registro.filial
				historico.actualizado_por = request.user
				historico.modificado_por = request.user
				
				historico.save()
				fecha = datetime.datetime.today()
				unida = "%s-%s-%s %s" % (fecha.year, fecha.month, fecha.day,  request.POST['hora-inicio']) 

				gestion = Gestion.objects.get(cliente_rechazado=historico)
				gestion.agente = request.user
				gestion.cliente_localizado = historico
				gestion.cliente_rechazado = None
				gestion.telefono = request.POST['telefono']
				gestion.hora_incio = unida
				gestion.tipo_gestion = 1
				gestion.save()


			formulario = ClienteActualizarForm()
			formulario2 = ClienteHistoricoForm()
			clientes = ClienteActualizar.objects.filter(agente=request.user, actualizado=False, codigo_rechazo__isnull= True, gestion__cliente_pendiente__isnull=True).order_by('-fecha_actualizacion')[:5]
			clientes_pendientes = Gestion.objects.filter(cliente_pendiente__isnull=False, agente=request.user).exclude(devolver_llamada__isnull=True).extra({'fecha_cast': "CAST(DevolverLlamada as DATE)"}).order_by('fecha_cast')[:5]
		
			clientes_rechazados = Gestion.objects.filter(cliente_rechazado__isnull=False, agente=request.user).order_by('-hora_final')[:5]
			ctx={
				'formulario': formulario,
				'formulario2': formulario2,
				'clientes': clientes,
				'clientes_pendientes': clientes_pendientes,
				'clientes_rechazados': clientes_rechazados,
				'gestiones': gestiones,
				'recordatorios': recordatorios,
			}
			return render(request, 'prospectacion/prestamos_fiduciarios.html', ctx)
		elif request.POST['metodo'] == 'pendiente':
			cliente = ClienteActualizar.objects.get(id=request.POST['cliente'])

			fecha = datetime.datetime.today()
			unida = "%s-%s-%s %s" % (fecha.year, fecha.month, fecha.day,  request.POST['hora-inicio']) 
			
			try:
				gestiones_anteriores = Gestion.objects.filter(cliente_pendiente=cliente)
				gestiones_anteriores.delete() 
			except Exception, e:
				pass

			print fecha

			if request.POST.get('tiempo') == 'pm':
				devolver_llamada = "%s %s%s:00" % (request.POST.get('fecha'), (int(request.POST.get('hora')) + 12), request.POST.get('minuto') )
			else:
				devolver_llamada = "%s %s%s:00" % (request.POST.get('fecha'), request.POST.get('hora'), request.POST.get('minuto') )
			
			date_object = datetime.datetime.strptime(devolver_llamada, '%Y-%m-%d %H:%M:%S')
			

			gestion = Gestion()
			gestion.agente = request.user
			gestion.cliente_pendiente = cliente
			gestion.telefono = request.POST['telefono']
			gestion.hora_incio = unida
			gestion.tipo_gestion = 3
			gestion.identidad = cliente.identidad
			gestion.cliente = cliente.id
			gestion.telefono_contacto = request.POST.get('numero_contacto')
			gestion.nombre_contacto = request.POST.get('nombre_contacto')
			gestion.devolver_llamada = devolver_llamada
			gestion.save()

			clientes = ClienteActualizar.objects.filter(agente=request.user, actualizado=False, codigo_rechazo__isnull= True, gestion__cliente_pendiente__isnull=True).order_by('-fecha_actualizacion')[:5]
			clientes_pendientes = Gestion.objects.filter(cliente_pendiente__isnull=False, agente=request.user).exclude(devolver_llamada__isnull=True).extra({'fecha_cast': "CAST(DevolverLlamada as DATE)"}).order_by('fecha_cast')[:5]
			clientes_rechazados = Gestion.objects.filter(cliente_rechazado__isnull=False, agente=request.user).order_by('-hora_final')[:5]
			
			formulario = ClienteActualizarForm()
			formulario2 = ClienteHistoricoForm()
			ctx={
				'formulario': formulario,
				'formulario2': formulario2,
				'clientes': clientes,
				'clientes_pendientes': clientes_pendientes,
				'clientes_rechazados': clientes_rechazados,
			}
			return render(request, 'prospectacion/prestamos_fiduciarios.html', ctx)

