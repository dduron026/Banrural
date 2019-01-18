# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import *
from django.template import RequestContext
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from cliente.forms import *
from django.db import transaction, IntegrityError
from django.db.models import Count, CharField, Case, Value, When, Sum, IntegerField, Q
from django.db import connection
from django.utils import timezone
from cobranzas.models import *
from cobranzas.forms import *

import time
import datetime
import json
import decimal


#------------------------------------------------------------------------------------------------------
#Convertir las fechas en formato que el JSON pueda reconocerlo
def date_handler(obj):
	if hasattr(obj, 'isoformat'):
		return obj.isoformat()
	else:
		raise TypeError

#Convertir los decimales en formato que el JSON pueda reconocerlo
def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)

#Convertir en diccionarios los cursores [{campo : valor1, campo2: valor2}]
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0].decode('utf8') for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

#obtener todas las gestiones
def obtener_gestiones(user):
	#El conteo de las gestiones
	gestiones = ClientesGestiones.objects.values(
		'agente',
		'agente__first_name',
		'agente__last_name',
	).filter(agente__id=user).extra(
		where=["CONVERT(varchar(10), FechaInicio, 105)= CONVERT(varchar(10), %s , 105)"], params=[datetime.datetime.today()]
	).annotate(
		total_localizado=Sum(
			Case(
				When(resultado_gestion__resultado_gestion=1, then=1),
				output_field=IntegerField(),
				)
			),
		total_no_localizado=Sum(
			Case(
				When(resultado_gestion__resultado_gestion=2, then=1),
				output_field=IntegerField(),
				)
			),
		total_pendiente=Sum(
			Case(
				When(resultado_gestion__resultado_gestion=3, then=1),
				output_field=IntegerField(),
				)
			),
		total=Count('resultado_gestion'),
	)
	return gestiones

#contar la mora y clientes:
def obtener_mora(user, pestana):
	try:
		mora = Clientes.objects.values(
			'agente',
			'agente__first_name',
			'agente__last_name',
		).filter(
			agente__id=user, 
			pestana=pestana
		).annotate(
			capital_mora=Sum('capital_mora'),
			intereses_mora=Sum('intereses_mora'),
			intereses_moratorios=Sum('intereses_moratorios'),
			saldo_total_creditos=Sum('saldo_total_creditos'),
			clientes=Count('cliente'),
		)[:1].get()
	except Exception as e:
		mora = {
			'capital_mora': 0,
			'intereses_mora': 0,
			'intereses_moratorios': 0,
			'saldo_total_creditos': 0,
			'clientes': 0
		}


	return mora



#------------------------------------------------------------------------------------------------------
#Pantalla principal donde muestra el listado de clientes para llamar
@login_required()
def morosidad_primera_cuota(request):
	#Borrar de la sesion toda la data
	try:
		del request.session['cuentas']
		del request.session['creditos']
		del request.session['pagos']
		del request.session['gestiones_cliente']
		del request.session['transacciones_tarjetas']
		del request.session['promesa_pago']
		del request.session['referencias']
		del request.session['tarjetas']
	except Exception as e:
		pass


	fecha = datetime.datetime.today()
	#Recordatorios
	gest= ClientesGestiones.objects.filter(resultado_gestion=3, agente=request.user)
	recordatorios = []
	for gestion in gest:
		if fecha >= gestion.devolver_llamada:
			recordatorios.append({'cliente': gestion.cliente.nombre , 'fecha': gestion.devolver_llamada.strftime('%Y-%m-%d %I:%M:%S%p')})

	

	gestiones= obtener_gestiones(request.user.id)
	if request.is_ajax():

		id = request.GET['id']
		try:
			from django.db import connection
			cursor = connection.cursor()
			
			#Traer la Informacion General de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetInformacionGeneral](%s)"%id
				cursor.execute(query)
				persona = dictfetchall(cursor)
				request.session['persona'] = persona
			except Exception as e:
				print e
				persona = False

			#Traer las referencias de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetReferenciasCliente](%s)"%id
				cursor.execute(query)
				referencias = dictfetchall(cursor)
				request.session['referencias'] = referencias
			except Exception as e:
				print e
				referencias = False

			#Traer las CUENTAS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetCuentasCliente](%s)"%id
				cursor.execute(query)
				cuentas = dictfetchall(cursor)
				request.session['cuentas'] = cuentas
				request.session['lacuenta'] = float(request.session['cuentas'][0]['saldo'].replace(',',''))
			except Exception as e:
				cuentas = False


			#Traer los CREDITOS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetCreditosCliente](%s)"%id
				cursor.execute(query)
				creditos = dictfetchall(cursor)
				request.session['creditos'] = creditos
			except Exception as e:
				print e
				creditos = False



			#Traer los CREDITOS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetTransaccionesTarjetasCliente](%s)"%id
				cursor.execute(query)
				transacciones_tarjetas = dictfetchall(cursor)
				request.session['transacciones_tarjetas'] = transacciones_tarjetas
			except Exception as e:
				print e
				transacciones_tarjetas = False

			#Traer el historial del credito seleccionado

			try:
				#query = "EXEC [dbo].[ConsultaSaldosTarjetas] @CodigoCliente ='%s'"%id
				query = "SELECT * FROM [dbo].[ConsultaSaldosTarjetaCliente]  ('%s')"%id
				cursor.execute(query)
				tarjetas = dictfetchall(cursor)
				request.session['tarjetas'] = tarjetas

			except Exception as e:
				print e, 'ESTE ERROR BASTRUQUIS'
				tarjetas = False

			

			#Traer los PAGOS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetPagosCliente](%s) ORDER BY CONVERT(DATE, fecha, 105) DESC"%id
				cursor.execute(query)
				pagos = dictfetchall(cursor)
				request.session['pagos'] = pagos
				#print pagos
			except Exception as e:
				print e
				pagos = False
			finally:
				cursor.close()

			#Trae todas las GESTIONES QUE HAN SIDO HECHAS POR EL CLIENTE
			try:
				gestiones_cliente = list(
					ClientesGestiones.objects.filter(cliente__cliente_id=id).extra(
						{
							'inicio': "CONVERT(varchar(15), FechaInicio, 105)", 
							'final': "CONVERT(varchar(15), FechaFinal, 105)", 
							'hora_inicio': "CONVERT(varchar(15), FechaInicio, 108)", 
							'hora_final': "CONVERT(varchar(15), FechaFinal, 108)",
							'monto_promesa': "CAST(MontoPromesa as varchar(15))"
						}).values(
							'tipo_gestion__descripcion', 
							'resultado_gestion__descripcion', 
							'telefono__telefono', 
							'agente__username', 
							'inicio', 
							'final', 
							'hora_inicio', 
							'hora_final',
							'observaciones',
							'nombre_gestor',
							'monto_promesa'
						).order_by('-fecha_inicio')
					)
				request.session['gestiones_cliente'] = gestiones_cliente
			except Exception as e:
				gestiones_cliente = False
				pass

			try:
				promesa_pago = list(
					ClientesPromesas.objects.filter(cliente__cliente_id=id).extra(
						{
							'fecha_promesa': "CONVERT(varchar(15), Fecha, 105)", 
							'fecha_gestion': "CONVERT(varchar(15), FechaGestion, 105)", 
							'hora_gestion': "CONVERT(varchar(15), FechaGestion, 108)",
							'monto_promesa': "CAST(MontoPromesa as varchar(15))"
						}).values(
							'agente__username', 
							'fecha_promesa', 
							'fecha_gestion', 
							'hora_gestion', 
							'estado',
							'nombre_agente',
							'monto_promesa'
						).order_by('-fecha')
					)
				request.session['promesa_pago'] = promesa_pago
			except Exception as e:
				promesa_pago = False
				pass

		except Exception, e:
			print e
			persona = False
			gestiones = False
			cuentas = False
			creditos = False
			transacciones_tarjetas = False
			pagos = False
			gestiones_cliente = False
			promesa_pago = False
			referencias = False


		data = {
			'gestiones': gestiones,
			'gestiones_cliente': gestiones_cliente,
			'persona': persona, #[{str(row) : val} for row, val in persona]
			'cuentas' : cuentas,
			'creditos' : creditos,
			'transacciones_tarjetas' : transacciones_tarjetas,
			'pagos' : pagos,
			'promesa_pago' : promesa_pago,
			'tarjetas' : tarjetas,
			'referencias' : referencias,
		}

		return HttpResponse(json.dumps(data, default=decimal_default), content_type='application/json')
	elif request.method == 'GET':
		request.session['url'] = '/cobranzas/'
		clientes = Clientes.objects.filter(agente=request.user, pestana=1, saldo_total_creditos__gte=0, hoy_actualizado=False, tiene_promesa = False, status=True)#.filter( cliente_gestion__fecha_inicio__lte=fecha)#.extra({'capital': "CAST(CapitalMora as DECIMAL(14,2))"}).order_by('capital')#, cliente_telefono__isnull=False).distinct()
		clientes_promesa = ClientesPromesas.objects.filter(cliente__pestana=1, cliente__status=1,  cliente__agente=request.user, estado='PENDIENTE', fecha__gte=datetime.date.today()).exclude(cod_gestion__fecha_gestion=datetime.date.today())
		clientes_pendientes = ClientesGestiones.objects.filter(resultado_gestion=3, agente=request.user, cliente__pestana=1).extra({'fecha_cast': "CAST(DevolverLlamada as DATE)"}).order_by('fecha_cast')[:15]
		ctx={
			'clientes': clientes,
			'clientes_pendientes': clientes_pendientes,
			'clientes_promesa': clientes_promesa,
			'gestiones': gestiones,
			'recordatorios': recordatorios,
			'numeroClientes':clientes.count(),
			'promesa': ClientesPromesas.objects.filter(cliente__pestana=1, cliente__status=1, cliente__agente=request.user, estado='PENDIENTE', fecha=datetime.date.today()).exclude(cod_gestion__fecha_gestion=datetime.date.today()).count(),
			'hoy':datetime.date.today(),
			
			# 'persona':persona
		}
	elif request.method == 'POST':
		request.session['url'] = '/cobranzas/'

		clientes= Clientes.objects.filter(dias_atraso=request.POST['diasAtraso'], agente=request.user, pestana=1,saldo_total_creditos__gte=0, hoy_actualizado=False, tiene_promesa = False, status=True)
		clientes_promesa = ClientesPromesas.objects.filter(cliente__pestana=1, cliente__status=1, cliente__agente=request.user, estado='PENDIENTE', fecha__gte=datetime.date.today()).exclude(cod_gestion__fecha_gestion=datetime.date.today())
		clientes_pendientes = ClientesGestiones.objects.filter(resultado_gestion=3, agente=request.user, cliente__pestana=1).extra({'fecha_cast': "CAST(DevolverLlamada as DATE)"}).order_by('fecha_cast')[:15]
		
		ctx={
			'clientes': clientes,
			'clientes_pendientes': clientes_pendientes,
			'clientes_promesa': clientes_promesa,
			'recordatorios':recordatorios,
			'numeroClientes':clientes.count(),
			'promesa': ClientesPromesas.objects.filter(cliente__pestana=1, cliente__status=1, cliente__agente=request.user, estado='PENDIENTE', fecha=datetime.date.today()).exclude(cod_gestion__fecha_gestion=datetime.date.today()).count(),
			'hoy':datetime.date.today(),
		}

	return render(request, 'morosidad_primera_cuota.html', ctx)

#Pantalla donde sale los numeros de telefonos del cliente que se selecciono
@login_required()
@transaction.atomic
def gestion(request, id):
	import time
	print "LA URL ACTUAL TIENE QUE SER LA DE PREMORA",request.session['url']
	try:
		cliente =  Clientes.objects.get(cliente= id)
	except Exception as e:
		raise e

	telefonos = ClientesTelefono.objects.filter(cliente=id)
	tipo_telefono = TiposTelefonos.objects.all()
	mensaje = ""
	gestiones= obtener_gestiones(request.user.id)

	if request.POST:
		if request.POST.get('metodo') == 'mensaje':
			telefono = request.POST['telefono'].replace('-', '') 
			if len(telefono) == 8:

				date_object = datetime.datetime.today()

				from django.db import connection
				with connection.cursor() as cursor:
					cursor.execute("EXEC [ADSYSPROC\SQL2008].SMSServer.dbo.InsertSMSFromCRM   @MessageTo='+504%s', @MessageFrom = 'BANRURAL', @MessageText ='%s'"%( request.POST['telefono'] , request.POST['mensaje'] ))
					cursor.execute("SELECT 1 ")
					row = cursor.fetchone()

					gestion = ClientesGestiones()
					gestion.cliente = Clientes.objects.get(cliente=id)
					gestion.cliente_interno = Clientes.objects.get(cliente=id).cliente_interno

					gestion.tipo_gestion = TiposGestion.objects.get(tipo_gestion = 2) #Mensaje
					gestion.resultado_gestion = ResultadoGestion.objects.get(resultado_gestion=9) #No localizado
					
					gestion.observaciones = request.POST.get('comentarios')
					gestion.mensaje = request.POST.get('mensaje')
					gestion.telefono = ClientesTelefono.objects.filter(cliente=id, telefono=request.POST.get('telefono'))[:1].get()
					gestion.fecha_inicio = date_object
					gestion.agente = request.user
					gestion.fecha_gestion =  time.strftime("%Y-%m-%d")
					gestion.save()

					#actualiza el campo de HoyActualizado para quitarlo de la lista de llamadas en el dia
					cliente_interno = Clientes.objects.get(cliente=id).cliente_interno
					clientes = Clientes.objects.filter(cliente_interno=cliente_interno)
					for cliente in clientes:
						cliente.hoy_actualizado = True
						cliente.save()

					mensaje = 'exito'
			else:
				mensaje = 'error'
		else:
			from distutils.util import strtobool
			try:
				with transaction.atomic():
					registro = ClientesTelefono()
					registro.cliente = Clientes.objects.get(cliente=id)
					registro.tipo_telefono = TiposTelefonos.objects.get(tipotelefono=request.POST.get('tipo_telefono')) 
					registro.telefono = request.POST.get('telefono')
					registro.mensaje = strtobool(request.POST.get('mensaje'))
					registro.activo = True
					registro.persona_referida = request.POST.get('persona_referida')
					registro.save()


			except Exception as e:
				#raise e
				mensaje = 'error'

			ctx={
				'mensaje' : mensaje,
				'cliente': cliente,
				'telefonos': telefonos,
				'tipo_telefono':tipo_telefono,
				'gestiones': gestiones
			}

	ctx={
		'mensaje' : mensaje,
		'cliente': cliente,
		'telefonos': telefonos,
		'tipo_telefono':tipo_telefono,
		'gestiones': gestiones
	}
	return render(request, 'gestion.html', ctx)


#Pantalla donde sale las opcion de localizado y no localizado
@login_required()
@transaction.atomic
def gestion_llamar(request, id, tel):
	import time
	#Se selecciona todas las gestiones que el agente ha realizado
	gestiones= obtener_gestiones(request.user.id)
	if request.POST:
		#El post solo vale cuando el cliente NO FUE LOCALIZADO
		date_object = datetime.datetime.strptime(str(datetime.date.today()) + ' ' + request.POST['hora-inicio']+'.000000', '%Y-%m-%d %H:%M:%S.%f')
		try:
			with transaction.atomic():
				#Se eliminan los pendientes anteriores, si existe
				try:
					gestiones_anteriores = ClientesGestiones.objects.filter(cliente=id, resultado_gestion=3)
					gestiones_anteriores.delete()
				except Exception, e:
					pass

				gestion = ClientesGestiones()
				gestion.cliente = Clientes.objects.get(cliente=id)
				gestion.cliente_interno = Clientes.objects.get(cliente=id).cliente_interno

				gestion.tipo_gestion = TiposGestion.objects.get(tipo_gestion = 1) #Llamada
				gestion.resultado_gestion = ResultadoGestion.objects.get(resultado_gestion=2) #No localizado
				gestion.telefono = ClientesTelefono.objects.filter(cliente=id, telefono=tel)[:1].get()
				gestion.observaciones = request.POST['comentarios']
				gestion.razon = request.POST['razon']
				gestion.fecha_inicio = date_object
				gestion.fecha_gestion =  time.strftime("%Y-%m-%d")
				gestion.agente = request.user
				gestion.save()

				#actualiza el campo de HoyActualizado para quitarlo de la lista de llamadas en el dia
				cliente_interno = Clientes.objects.get(cliente=id).cliente_interno
				clientes = Clientes.objects.filter(cliente_interno=cliente_interno)
				for cliente in clientes:
					cliente.hoy_actualizado = True
					cliente.save()


				return redirect(request.session['url'])
		except Exception as e:
			raise e
	else:
		cliente =  Clientes.objects.get(cliente= id)
		telefonos = ClientesTelefono.objects.filter(cliente=id)

		ctx={
			'cliente': cliente,
			'telefonos': telefonos,
			'gestiones': gestiones,
			'tel':tel,
		}
	return render(request, 'gestion_llamar.html', ctx)


#Pantalla donde el cliente es localizado y responde las preguntas
@login_required()
@transaction.atomic
def gestion_localizado(request, id, tel):
	gestiones= obtener_gestiones(request.user.id)
	agencias = Agencias.objects.all().order_by('nombre_agencia')
	if request.POST:
		#Si el cliente contesta normal
		date_object = datetime.datetime.strptime(str(datetime.date.today()) + ' ' + request.POST['hora-inicio']+'.000000', '%Y-%m-%d %H:%M:%S.%f')
		if request.POST['metodo'] == 'localizado':
			#Se eliminan los pendientes anteriores, si existe
			try:
				gestiones_anteriores = ClientesGestiones.objects.filter(cliente=id, resultado_gestion=3)
				gestiones_anteriores.delete()
			except Exception, e:
				pass

			try:
				with transaction.atomic():
					#Guarda la gestion del cliente
					gestion = ClientesGestiones()
					gestion.cliente = Clientes.objects.get(cliente=id)
					gestion.tipo_gestion = TiposGestion.objects.get(tipo_gestion = 1) #Llamada
					gestion.cliente_interno = Clientes.objects.get(cliente=id).cliente_interno
					gestion.resultado_gestion = ResultadoGestion.objects.get(resultado_gestion=1) #localizado
					gestion.telefono = ClientesTelefono.objects.filter(cliente=id, telefono=tel)[:1].get()
					gestion.observaciones = request.POST['observaciones']
					gestion.razon = request.POST['opcion'] #Si pagara o no, los radios button
					gestion.fecha_gestion =  time.strftime("%Y-%m-%d")

					try:
						gestion.resultado_razon = request.POST['razon_opcion'] #Esta opcion son las fechas
						gestion.monto_promesa =  None if  request.POST.get('monto_promesa') == '' else request.POST.get('monto_promesa') 
						

					except Exception as e:
						pass
					gestion.fecha_inicio = date_object
					print "----------------------------------",gestion.fecha_inicio
					gestion.agente = request.user
					gestion.save()

					#actualiza el campo de HoyActualizado para quitarlo de la lista de llamadas en el dia
					cliente_interno = Clientes.objects.get(cliente=id).cliente_interno
					clientes = Clientes.objects.filter(cliente_interno=cliente_interno)
					for cliente in clientes:
						cliente.hoy_actualizado = True
						cliente.save()


					#Guarda la promesa de pago
					if request.POST['opcion'] == '1':
						promesa = ClientesPromesas()
						promesa.cliente = Clientes.objects.get(cliente=id)
						promesa.fecha = request.POST['razon_opcion']
						promesa.agente = request.user
						promesa.estado = 'PENDIENTE'
						promesa.cod_gestion = gestion
						promesa.cliente_interno = Clientes.objects.get(cliente=id).cliente_interno
						promesa.monto_promesa = None if  request.POST.get('monto_promesa') == '' else request.POST.get('monto_promesa')
						promesa.cuota = gestion.cliente.cuota
						promesa.save()

						#actualiza el cliente que tiene una promesa de pago activa, para que no aparezca en el listado de llamadas
						cliente.tiene_promesa = True
						cliente.save()

					if request.POST['opcion'] == '2':
						promesa = ClientesPromesas()
						promesa.cliente = Clientes.objects.get(cliente=id)
						promesa.fecha = datetime.date.today()+datetime.timedelta(days=7)
						promesa.agente = request.user
						promesa.estado = 'PENDIENTE'
						promesa.cliente_interno = Clientes.objects.get(cliente=id).cliente_interno
						promesa.cod_gestion = gestion
						promesa.cuota = gestion.cliente.cuota
						promesa.save()

						#actualiza el cliente que tiene una promesa de pago activa, para que no aparezca en el listado de llamadas
						cliente.tiene_promesa = True
						cliente.save()

					print request.session['url']
					return redirect(request.session['url'])
			except Exception as e:
				raise e
				mensaje = 'error'
		elif request.POST['metodo'] == 'pendiente':
			#Se eliminan los pendientes anteriores, si existe
			try:
				gestiones_anteriores = ClientesGestiones.objects.filter(cliente=id,resultado_gestion=3)
				gestiones_anteriores.delete()
			except Exception, e:
				pass
			#Se construye la fecha y hora dependiendo de los datos seleccionados
			if request.POST.get('tiempo') == 'pm':
				devolver_llamada = "%s %s%s:00" % (request.POST.get('fecha'), (int(request.POST.get('hora')) + 12), request.POST.get('minuto') )
			else:
				devolver_llamada = "%s %s%s:00" % (request.POST.get('fecha'), request.POST.get('hora'), request.POST.get('minuto') )

			try:
				with transaction.atomic():
					gestion = ClientesGestiones()
					gestion.cliente = Clientes.objects.get(cliente=id)
					gestion.cliente_interno = Clientes.objects.get(cliente=id).cliente_interno
					gestion.tipo_gestion = TiposGestion.objects.get(tipo_gestion = 1) #Llamada
					gestion.resultado_gestion = ResultadoGestion.objects.get(resultado_gestion=3) #Pendiente
					gestion.telefono = ClientesTelefono.objects.filter(cliente=id, telefono=tel)[:1].get()
					gestion.fecha_gestion =  time.strftime("%Y-%m-%d")


					gestion.fecha_inicio = date_object

					print "----------------------------------",gestion.fecha_inicio
					gestion.devolver_llamada = devolver_llamada
					gestion.nombre_contacto = request.POST.get('nombre_contacto')
					gestion.telefono_contacto = request.POST.get('telefono_contacto')
					gestion.agente = request.user

					gestion.save()

					return redirect(request.session['url'])
			except Exception as e:
				raise e
				mensaje = 'error'
		elif request.POST['metodo'] == 'telefono':
			from distutils.util import strtobool
			try:
				with transaction.atomic():
					gestion = ClientesTelefono()
					gestion.cliente = Clientes.objects.get(cliente=id)
					gestion.tipo_telefono = TiposTelefonos.objects.get(tipotelefono=request.POST['tipo_telefono'])
					gestion.telefono = request.POST['telefono']
					gestion.mensaje = strtobool(request.POST['mensaje'])
					gestion.activo = True
					gestion.persona_referida = request.POST['persona_referida']
					gestion.save()

					cliente =  Clientes.objects.get(cliente= id)
					telefonos = ClientesTelefono.objects.filter(cliente=id)
					tipo_telefono = TiposTelefonos.objects.all()
			except Exception as e:
				raise e
				mensaje = 'error'

	else:
		cliente =  Clientes.objects.get(cliente= id)
		telefonos = ClientesTelefono.objects.filter(cliente=id)
		tipo_telefono = TiposTelefonos.objects.all()
	ctx={
		'cliente': cliente,
		'telefonos': telefonos,
		'tel':tel,
		'tipo_telefono': tipo_telefono,
		'gestiones': gestiones,
		'agencias':agencias
	}
	return render(request, 'gestion_localizado.html', ctx)


#Pantalla donde el cliente es localizado y responde las preguntas
@login_required()
def gestion_ajax(request):
	print "SEEEEEEEEE METIOOOOA L AJAAAAAAX",request.session['url']
	data = {}
	from django.db import connection
	cursor = connection.cursor()
	if request.GET['opcion'] == 'historial':
		print "Entre al historial"

		
		id = request.GET['credito']
		#Traer el historial del credito seleccionado
		try:
			query = "SELECT TOP 100 * FROM [CCCOB].[fnGetHistorialPagoCliente]('%s') ORDER BY CONVERT(DATE, fecha, 105) DESC"%id
			cursor.execute(query)
			historial = dictfetchall(cursor)
		except Exception as e:
			historial = e
			pass
		finally:
			cursor.close()
		data = {
			'historial':historial,
		}

	if request.GET['opcion'] == 'plan_pago':
		id = request.GET['credito']
		#Traer el historial del credito seleccionado
		try:
			query = "SELECT * FROM [CCCOB].[fnGetPlanPagoCliente]('%s') ORDER BY CONVERT(DATE, fecha, 105) ASC"%id
			cursor.execute(query)
			plan = dictfetchall(cursor)
		except Exception as e:
			plan = e
			pass
		finally:
			cursor.close()
		data = {
			'plan':plan
		}


	if request.GET['opcion'] == 'monto_desembolsado':
		id = Clientes.objects.filter(credito=request.GET['credito'])[:1].get().cliente_id

		#Traer el historial del credito seleccionado

		try:
			query = "SELECT * FROM [CCCOB].[fnGetCreditosCliente](%s)"%id
			cursor.execute(query)
			creditos = dictfetchall(cursor)
			request.session['creditos'] = creditos

		except Exception as e:
			creditos = False

		try:
			id = request.GET['credito']

			queryGarantias = "SELECT * FROM [CCCOB].[fnGetGarantiaCredito]('%s')"%id
			cursor.execute(queryGarantias)
			garantias = dictfetchall(cursor)
			request.session['garantias'] = garantias
		except Exception as e:
			garantias = False

		finally:
			cursor.close()
		data = {
			'creditos':creditos,
			'garantias':garantias,

		}

	return HttpResponse(json.dumps(data, default=decimal_default), content_type='application/json')


#Aqui es el boton de cargar nuevamente la informacion de los clientes
@login_required()
def cargar_informacion(request, id):
	if request.is_ajax():
		id = request.GET['id']
		try:
			#AQUI PONE EN SESION TODAS LOS DETALLES DEL CLIENTE
			from django.db import connection
			cursor = connection.cursor()
			
			#Traer la Informacion General de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetInformacionGeneral](%s)"%id
				cursor.execute(query)
				persona = dictfetchall(cursor)
				request.session['persona'] = persona
			except Exception as e:
				print e
				persona = False

			#Traer las CUENTAS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetCuentasCliente](%s)"%id
				cursor.execute(query)
				cuentas = dictfetchall(cursor)
				request.session['cuentas'] = cuentas
				request.session['lacuenta'] = float(request.session['cuentas'][0]['saldo'].replace(',',''))
			except Exception as e:
				cuentas = False


			#Traer los CREDITOS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetCreditosCliente](%s)"%id
				cursor.execute(query)
				creditos = dictfetchall(cursor)
				request.session['creditos'] = creditos
			except Exception as e:
				print e 
				creditos = False

			#Traer los CREDITOS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetTransaccionesTarjetasCliente](%s)"%id
				cursor.execute(query)
				transacciones_tarjetas = dictfetchall(cursor)
				request.session['transacciones_tarjetas'] = transacciones_tarjetas
				#print transacciones_tarjetas
			except Exception as e:
				print e
				transacciones_tarjetas = False


			#Traer los CREDITOS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetPagosCliente](%s) ORDER BY CONVERT(DATE, fecha, 105) DESC"%id
				cursor.execute(query)
				pagos = dictfetchall(cursor)
				request.session['pagos'] = pagos
				#print pagos
			except Exception as e:
				print e
				pagos = False
			finally:
				cursor.close()

			#Trae todas las GESTIONES QUE HAN SIDO HECHAS POR EL CLIENTE
			try:
				gestiones_cliente = list(
					ClientesGestiones.objects.filter(cliente__cliente_id=id).extra(
						{
							'inicio': "CONVERT(varchar(15), FechaInicio, 105)", 
							'final': "CONVERT(varchar(15), FechaFinal, 105)", 
							'hora_inicio': "CONVERT(varchar(15), FechaInicio, 108)", 
							'hora_final': "CONVERT(varchar(15), FechaFinal, 108)",

						}).values(
							'tipo_gestion__descripcion', 
							'resultado_gestion__descripcion', 
							'telefono__telefono', 
							'agente__username', 
							'inicio', 
							'final', 
							'hora_inicio', 
							'hora_final',
							'observaciones',
							'nombre_gestor',
							'monto_promesa'
						)
					)
				request.session['gestiones_cliente'] = gestiones_cliente
			except Exception as e:
				print e
				gestiones_cliente = False
				pass

		except Exception, e:
			print e
			persona = False
			gestiones = False
			cuentas = False
			creditos = False
			transacciones_tarjetas = False
			pagos = False
			gestiones_cliente = False


		data = {
			'gestiones': gestiones,
			'gestiones_cliente': gestiones_cliente,
			'persona': persona, #[{str(row) : val} for row, val in persona]
			'cuentas' : cuentas,
			'creditos' : creditos,
			'transacciones_tarjetas' : transacciones_tarjetas,
			'pagos' : pagos,
		}

		return HttpResponse(json.dumps(data, default=decimal_default), content_type='application/json')


#Pantalla principal donde muestra el listado de clientes para llamar
@login_required()
def opcion2(request):
	#Borrar de la sesion toda la data
	try:
		del request.session['cuentas']
		del request.session['creditos']
		del request.session['pagos']
		del request.session['gestiones_cliente']
		del request.session['transacciones_tarjetas']
		del request.session['promesa_pago']
	except Exception as e:
		pass

	fecha = datetime.datetime.today()
	#Recordatorios
	gest= ClientesGestiones.objects.filter(resultado_gestion=3, agente=request.user)
	recordatorios = []
	for gestion in gest:
		if fecha >= gestion.devolver_llamada:
			recordatorios.append({'cliente': gestion.cliente.nombre , 'fecha': gestion.devolver_llamada.strftime('%Y-%m-%d %I:%M:%S%p')})

	
	request.session['url'] = '/cobranzas/banrural/'

	#Llama el metodo de las gestiones
	gestiones= obtener_gestiones(request.user.id)
	if request.is_ajax():
		id = request.GET['id']
		try:
			#AQUI PONE EN SESION TODAS LOS DETALLES DEL CLIENTE
			from django.db import connection
			cursor = connection.cursor()

			#Traer las CUENTAS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetCuentasCliente](%s)"%id
				cursor.execute(query)
				cuentas = dictfetchall(cursor)
				request.session['cuentas'] = cuentas
			except Exception as e:
				cuentas = False


			#Traer los CREDITOS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetCreditosCliente](%s)"%id
				cursor.execute(query)
				creditos = dictfetchall(cursor)
				request.session['creditos'] = creditos
				#print creditos
			except Exception as e:
				print e
				creditos = False

			#Traer los CREDITOS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetTransaccionesTarjetasCliente](%s)"%id
				cursor.execute(query)
				transacciones_tarjetas = dictfetchall(cursor)
				request.session['transacciones_tarjetas'] = transacciones_tarjetas
				#print transacciones_tarjetas
			except Exception as e:
				print e
				transacciones_tarjetas = False


			#Traer los CREDITOS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetPagosCliente](%s)"%id
				cursor.execute(query)
				pagos = dictfetchall(cursor)
				request.session['pagos'] = pagos
				#print pagos
			except Exception as e:
				print e
				pagos = False
			finally:
				cursor.close()

			#Trae todas las GESTIONES QUE HAN SIDO HECHAS POR EL CLIENTE
			try:
				gestiones_cliente = list(
					ClientesGestiones.objects.filter(cliente__cliente_id=id).extra(
						{
							'inicio': "CONVERT(varchar(15), FechaInicio, 105)", 
							'final': "CONVERT(varchar(15), FechaFinal, 105)", 
							'hora_inicio': "CONVERT(varchar(15), FechaInicio, 108)", 
							'hora_final': "CONVERT(varchar(15), FechaFinal, 108)"
						}).values(
							'tipo_gestion__descripcion', 
							'resultado_gestion__descripcion', 
							'telefono__telefono', 
							'agente__username', 
							'inicio', 
							'final', 
							'hora_inicio', 
							'hora_final',
							'observaciones',
							'nombre_gestor',
							'monto_promesa'
						).order_by('-fecha_inicio')
					)
				request.session['gestiones_cliente'] = gestiones_cliente
			except Exception as e:
				gestiones_cliente = False
				pass

			try:
				promesa_pago = list(
					ClientesPromesas.objects.filter(cliente__cliente_id=id).extra(
						{
							'fecha_promesa': "CONVERT(varchar(15), Fecha, 105)", 
							'fecha_gestion': "CONVERT(varchar(15), FechaGestion, 105)", 
							'hora_gestion': "CONVERT(varchar(15), FechaGestion, 108)"
						}).values(
							'agente__username', 
							'fecha_promesa', 
							'fecha_gestion', 
							'hora_gestion', 
							'estado',
							'nombre_agente'
							'monto_promesa'
						).order_by('-fecha')
					)
				request.session['promesa_pago'] = promesa_pago
			except Exception as e:
				promesa_pago = False
				pass

		except Exception, e:
			print e
			persona = False
			gestiones = False
			cuentas = False
			creditos = False
			transacciones_tarjetas = False
			pagos = False
			gestiones_cliente = False
			promesa_pago = False


		data = {
			'gestiones': gestiones,
			'gestiones_cliente': gestiones_cliente,
			'persona': persona, #[{str(row) : val} for row, val in persona]
			'cuentas' : cuentas,
			'creditos' : creditos,
			'transacciones_tarjetas' : transacciones_tarjetas,
			'pagos' : pagos,
			'promesa_pago' : promesa_pago,
		}

		return HttpResponse(json.dumps(data, default=decimal_default), content_type='application/json')
	elif request.method == 'GET':
		request.session['url'] = '/cobranzas/banrural/'
		clientes = Clientes.objects.filter(agente=request.user, pestana=2, saldo_total_creditos__gte=0, hoy_actualizado=False, tiene_promesa = False, status=True)#.filter( cliente_gestion__fecha_inicio__lte=fecha)#.extra({'capital': "CAST(CapitalMora as DECIMAL(14,2))"}).order_by('capital')#, cliente_telefono__isnull=False).distinct()
		clientes_pendientes = ClientesGestiones.objects.filter(resultado_gestion=3, agente=request.user,  cliente__pestana=2).extra({'fecha_cast': "CAST(DevolverLlamada as DATE)"}).order_by('fecha_cast')[:15]
		clientes_promesa = ClientesPromesas.objects.filter(cliente__pestana=2,  cliente__status=1, cliente__agente=request.user, estado='PENDIENTE', fecha__gte=datetime.date.today()).exclude(cod_gestion__fecha_gestion=datetime.date.today())
		
		formulario = ClienteActualizarForm()
		formulario2 = ClienteHistoricoForm()
		ctx={
			'formulario': formulario,
			'formulario2': formulario2,
			'clientes': clientes,
			'clientes_pendientes': clientes_pendientes,
			'gestiones': gestiones,
			'recordatorios': recordatorios,
			'numeroClientes':clientes.count(),
			'clientes_promesa': clientes_promesa,
			'promesa': ClientesPromesas.objects.filter(cliente__pestana=2, cliente__status=1, cliente__agente=request.user, estado='PENDIENTE', fecha=datetime.date.today()).exclude(cod_gestion__fecha_gestion=datetime.date.today()).count(),
			'hoy':datetime.date.today(),
		}

	elif request.method == 'POST':
		request.session['url'] = '/cobranzas/banrural/'
		clientes = Clientes.objects.filter(dias_atraso=request.POST['diasAtraso'], agente=request.user, pestana=2, saldo_total_creditos__gte=0, hoy_actualizado=False, tiene_promesa = False, status=True)#.filter( cliente_gestion__fecha_inicio__lte=fecha)#.extra({'capital': "CAST(CapitalMora as DECIMAL(14,2))"}).order_by('capital')#, cliente_telefono__isnull=False).distinct()
		clientes_pendientes = ClientesGestiones.objects.filter(resultado_gestion=3, agente=request.user, cliente__pestana=3).extra({'fecha_cast': "CAST(DevolverLlamada as DATE)"}).order_by('fecha_cast')[:15]
		clientes_promesa = ClientesPromesas.objects.filter(cliente__pestana=2, cliente__status=1, cliente__agente=request.user, estado='PENDIENTE', fecha__gte=datetime.date.today()).exclude(cod_gestion__fecha_gestion=datetime.date.today())
		
		ctx={
			'clientes': clientes,
			'clientes_pendientes': clientes_pendientes,
			'numeroClientes':clientes.count(),
			'clientes_promesa': clientes_promesa,
			'promesa': ClientesPromesas.objects.filter(cliente__pestana=2, cliente__status=1, cliente__agente=request.user, estado='PENDIENTE', fecha=datetime.date.today()).exclude(cod_gestion__fecha_gestion=datetime.date.today()).count(),
			'hoy':datetime.date.today(),
		}
	return render(request, 'opcion2.html', ctx)



		#Pantalla principal donde muestra el listado de clientes para llamar


#Pantalla principal donde muestra el listado de clientes para llamar
@login_required()
def opcion3(request):

	#Borrar de la sesion toda la data
	try:
		del request.session['cuentas']
		del request.session['creditos']
		del request.session['pagos']
		del request.session['gestiones_cliente']
		del request.session['transacciones_tarjetas']
		del request.session['promesa_pago']
	except Exception as e:
		pass


	import datetime
	fecha = datetime.datetime.today()
	#Recordatorios
	gest= ClientesGestiones.objects.filter(resultado_gestion=3, agente=request.user)
	recordatorios = []
	for gestion in gest:
		if fecha >= gestion.devolver_llamada:
			recordatorios.append({'cliente': gestion.cliente.nombre , 'fecha': gestion.devolver_llamada.strftime('%Y-%m-%d %I:%M:%S%p')})
	
	request.session['url'] = '/cobranzas/pre_mora/'

	#Llama el metodo de las gestiones
	gestiones= obtener_gestiones(request.user.id)
	if request.is_ajax():
		request.session['url'] = '/cobranzas/pre_mora/'
		id = request.GET['id']
		try:
			
			persona = dict(
				Clientes.objects.values(
					'cliente',
					'cliente_id',
					'nombre',
					'sexo',
					'correo_electronico',
					'identidad',
					'cant_creditos',
					'saldo_total_creditos',
					'capital_mora',
					'intereses_mora',
					'intereses_moratorios',
					'otros_recargos',
					'dias_atraso',
					'cuotas_mora'
				).get(cliente_id=id)
			)
			#AQUI PONE EN SESION TODAS LOS DETALLES DEL CLIENTE
			from django.db import connection
			cursor = connection.cursor()

			#Traer las CUENTAS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetCuentasCliente](%s)"%id
				cursor.execute(query)
				cuentas = dictfetchall(cursor)
				request.session['cuentas'] = cuentas
			except Exception as e:
				cuentas = False


			#Traer los CREDITOS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetCreditosCliente](%s)"%id
				cursor.execute(query)
				creditos = dictfetchall(cursor)
				request.session['creditos'] = creditos
				#print creditos
			except Exception as e:
				print e
				creditos = False

			#Traer los CREDITOS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetTransaccionesTarjetasCliente](%s)"%id
				cursor.execute(query)
				transacciones_tarjetas = dictfetchall(cursor)
				request.session['transacciones_tarjetas'] = transacciones_tarjetas
				#print transacciones_tarjetas
			except Exception as e:
				print e
				transacciones_tarjetas = False


			#Traer los CREDITOS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetPagosCliente](%s)"%id
				cursor.execute(query)
				pagos = dictfetchall(cursor)
				request.session['pagos'] = pagos
				#print pagos
			except Exception as e:
				print e
				pagos = False
			finally:
				cursor.close()

			#Trae todas las GESTIONES QUE HAN SIDO HECHAS POR EL CLIENTE
			try:
				gestiones_cliente = list(
					ClientesGestiones.objects.filter(cliente__cliente_id=id).extra(
						{
							'inicio': "CONVERT(varchar(15), FechaInicio, 105)", 
							'final': "CONVERT(varchar(15), FechaFinal, 105)", 
							'hora_inicio': "CONVERT(varchar(15), FechaInicio, 108)", 
							'hora_final': "CONVERT(varchar(15), FechaFinal, 108)"
						}).values(
							'tipo_gestion__descripcion', 
							'resultado_gestion__descripcion', 
							'telefono__telefono', 
							'agente__username', 
							'inicio', 
							'final', 
							'hora_inicio', 
							'hora_final',
							'observaciones',
							'nombre_gestor',
							'monto_promesa'
						).order_by('-fecha_inicio')
					)
				request.session['gestiones_cliente'] = gestiones_cliente
			except Exception as e:
				gestiones_cliente = False
				pass

			try:
				promesa_pago = list(
					ClientesPromesas.objects.filter(cliente__cliente_id=id).extra(
						{
							'fecha_promesa': "CONVERT(varchar(15), Fecha, 105)", 
							'fecha_gestion': "CONVERT(varchar(15), FechaGestion, 105)", 
							'hora_gestion': "CONVERT(varchar(15), FechaGestion, 108)",
							'monto_promesa': "CAST(MontoPromesa,varchar(15))"
						}).values(
							'agente__username', 
							'fecha_promesa', 
							'fecha_gestion', 
							'hora_gestion', 
							'estado',
							'nombre_agente',
							'monto_promesa'
						).order_by('-fecha')
					)
				request.session['promesa_pago'] = promesa_pago
			except Exception as e:
				promesa_pago = False
				pass

		except Exception, e:
			print e
			persona = False
			gestiones = False
			cuentas = False
			creditos = False
			transacciones_tarjetas = False
			pagos = False
			gestiones_cliente = False
			promesa_pago = False


		data = {
			'gestiones': gestiones,
			'gestiones_cliente': gestiones_cliente,
			'persona': persona, #[{str(row) : val} for row, val in persona]
			'cuentas' : cuentas,
			'creditos' : creditos,
			'transacciones_tarjetas' : transacciones_tarjetas,
			'pagos' : pagos,
			'promesa_pago' : promesa_pago,
		}

		return HttpResponse(json.dumps(data, default=decimal_default), content_type='application/json')
	elif request.method == 'GET':
		request.session['url'] = '/cobranzas/pre_mora/'
		from datetime import datetime, date

		if ('desde') not in request.session:
			clientes = Clientes.objects.filter(agente=request.user, pestana=3, proxima_fecha_pago__isnull=False, hoy_actualizado=False, tiene_promesa = False)#.filter( cliente_gestion__fecha_inicio__lte=fecha)#.extra({'capital': "CAST(CapitalMora as DECIMAL(14,2))"}).order_by('capital')#, cliente_telefono__isnull=False).distinct()

		else:
			from datetime import datetime, date
			clientes = Clientes.objects.filter(agente=request.user, pestana=3,  hoy_actualizado=False, tiene_promesa = False).filter(proxima_fecha_pago__range=(request.session['desde'], request.session['hasta']))#.filter( cliente_gestion__fecha_inicio__lte=fecha)#.extra({'capital': "CAST(CapitalMora as DECIMAL(14,2))"}).order_by('capital')#, cliente_telefono__isnull=False).distinct()
		

		clientes_pendientes = ClientesGestiones.objects.filter(resultado_gestion=3, agente=request.user, cliente__pestana=3).extra({'fecha_cast': "CAST(DevolverLlamada as DATE)"}).order_by('fecha_cast')[:15]
		clientes_promesa = ClientesPromesas.objects.filter(cliente__pestana=3, cliente__status=1, cliente__agente=request.user, estado='PENDIENTE', fecha__gte=date.today()).exclude(cod_gestion__fecha_gestion=date.today())
		
		#Para obtener por medio de distinct
	
		from django.db import connection
		cursor = connection.cursor()
		#Traer el historial del credito seleccionado
		try:
			query = "SELECT DISTINCT  [ProductoCredito]FROM [CRM].[CCCOB].[Clientes]"
			cursor.execute(query)
			productos = dictfetchall(cursor)
		except Exception as e:
			print e
			productos = False
			pass
		finally:
			cursor.close()

			

		formulario = ClienteActualizarForm()
		formulario2 = ClienteHistoricoForm()
		ctx={
			'formulario': formulario,
			'formulario2': formulario2,
			'clientes': clientes,
			'gestiones': gestiones,
			'numeroClientes':clientes.count(),
			'productos':productos,
			'clientes_promesa': clientes_promesa,
			'promesa': ClientesPromesas.objects.filter(cliente__pestana=3,  cliente__status=1,cliente__agente=request.user, estado='PENDIENTE', fecha=date.today()).exclude(cod_gestion__fecha_gestion=date.today()).count(),
			'hoy':date.today(),

		}
		return render(request, 'opcion3.html', ctx)
	elif request.method == 'POST':
		request.session['url'] = '/cobranzas/pre_mora/'
		from datetime import datetime, date


		request.session['desde'] = str(datetime.strptime(request.POST['desde'], '%Y-%m-%d').date())
		request.session['hasta'] = str(datetime.strptime(request.POST['hasta'], '%Y-%m-%d').date())


		clientes = Clientes.objects.filter(agente=request.user, pestana=3,  hoy_actualizado=False, tiene_promesa = False).filter(proxima_fecha_pago__range=(request.session['desde'], request.session['hasta']))#.filter( cliente_gestion__fecha_inicio__lte=fecha)#.extra({'capital': "CAST(CapitalMora as DECIMAL(14,2))"}).order_by('capital')#, cliente_telefono__isnull=False).distinct()
		clientes_pendientes = ClientesGestiones.objects.filter(resultado_gestion=3, agente=request.user , cliente__pestana=3).extra({'fecha_cast': "CAST(DevolverLlamada as DATE)"}).order_by('fecha_cast')[:15]
		clientes_promesa = ClientesPromesas.objects.filter(cliente__pestana=3,  cliente__status=1,cliente__agente=request.user, estado='PENDIENTE', fecha__gte=date.today()).exclude(cod_gestion__fecha_gestion=date.today())
		


		from django.db import connection
		cursor = connection.cursor()
		#Traer el historial del credito seleccionado
		try:
			query = "SELECT DISTINCT  [ProductoCredito]FROM [CRM].[CCCOB].[Clientes]"
			cursor.execute(query)
			productos = dictfetchall(cursor)
		except Exception as e:
			print e
			productos = False
			pass
		finally:
			cursor.close()

		formulario = ClienteActualizarForm()
		formulario2 = ClienteHistoricoForm()
		ctx={
			'formulario': formulario,
			'formulario2': formulario2,
			'clientes': clientes,
			'gestiones': gestiones,
			'recordatorios': recordatorios,
			'desde': request.POST['desde'],
			'hasta' : request.POST['hasta'],
			'numeroClientes':clientes.count(),
			'productos':productos,
			'clientes_promesa': clientes_promesa,
			'promesa': ClientesPromesas.objects.filter(cliente__pestana=3, cliente__status=1, cliente__agente=request.user, estado='PENDIENTE', fecha=date.today()).exclude(cod_gestion__fecha_gestion=date.today()).count(),
			'hoy':date.today(),
		}
		return render(request, 'opcion3.html', ctx)


#Aqui es el boton de cargar nuevamente la informacion de los clientes
@login_required()
def buscar_gestionados(request):
	#Llama el metodo de las gestiones
	gestiones= obtener_gestiones(request.user.id)
	ctx = {'gestiones':gestiones}

	request.session['url'] = '/cobranzas/buscar/gestionados/'

	if request.POST:
		try:
			print list(request.user.groups.values_list('name', flat=True).all()) 
			if request.user.is_superuser:
				cliente = Clientes.objects.filter(Q(identidad=request.POST['identidad']) | Q(credito=request.POST['identidad']) | Q(cliente_interno=request.POST['identidad']) | Q(nombre=request.POST['identidad']))[:1].get()
			elif 'Operador - BO' in list(request.user.groups.values_list('name', flat=True).all()) :
				cliente = Clientes.objects.filter(Q(identidad=request.POST['identidad']) | Q(credito=request.POST['identidad']) | Q(cliente_interno=request.POST['identidad']) | Q(nombre=request.POST['identidad']))[:1].get()
				url = '/cobranzasbo/gestionesbo/'+str(cliente.cliente)
				request.session['pagina_principal'] = '/cobranzas/buscar/gestionados/'
			else:
				cliente = Clientes.objects.filter(Q(identidad=request.POST['identidad']) | Q(credito=request.POST['identidad']) | Q(cliente_interno=request.POST['identidad']) | Q(nombre=request.POST['identidad'])).filter(agente__id = request.user.id)[:1].get()
				url = '/cobranzas/gestion/'+str(cliente.cliente)

			ctx = {
				'cliente' : cliente,
				'url' : url,
				'gestiones' : gestiones
			}
		except Exception as e:
			ctx = {
				'mensaje' : 'error',
				'gestiones' : gestiones
			}
	return render(request, 'buscar_gestionados.html', ctx)

@login_required()
def buscar_agente(request):
	#Llama el metodo de las gestiones
	gestiones= obtener_gestiones(request.user.id)
	ctx = {'gestiones':gestiones}

	request.session['url'] = '/cobranzas/buscar/agente/'

	if request.POST:
		try:
			if request.user.is_superuser:
				cliente = Clientes.objects.filter(Q(identidad=request.POST['identidad']) | Q(cliente_interno=request.POST['identidad']) | Q(nombre=request.POST['identidad']))[:1].get()
			elif 'Operador - Bancon' in list(request.user.groups.values_list('name', flat=True).all()) :
				cliente = Clientes.objects.filter(Q(identidad=request.POST['identidad']) | Q(cliente_interno=request.POST['identidad']) | Q(nombre=request.POST['identidad'])).filter(pestana=1)[:1].get()
			elif 'Operador - Banrural' in list(request.user.groups.values_list('name', flat=True).all()) :
				cliente = Clientes.objects.filter(Q(identidad=request.POST['identidad']) | Q(cliente_interno=request.POST['identidad']) | Q(nombre=request.POST['identidad'])).filter(pestana=2)[:1].get()
			elif 'Operador - Premora' in list(request.user.groups.values_list('name', flat=True).all()) :
				cliente = Clientes.objects.filter(Q(identidad=request.POST['identidad']) | Q(cliente_interno=request.POST['identidad']) | Q(nombre=request.POST['identidad'])).filter(pestana=3)[:1].get()
			elif 'Operador - BO' in list(request.user.groups.values_list('name', flat=True).all()) :
				cliente = Clientes.objects.filter(Q(identidad=request.POST['identidad']) | Q(cliente_interno=request.POST['identidad']) | Q(nombre=request.POST['identidad'])).filter(pestana=5)[:1].get()
			elif 'Operador - SUC' in list(request.user.groups.values_list('name', flat=True).all()) :
				cliente = Clientes.objects.filter(Q(identidad=request.POST['identidad']) | Q(cliente_interno=request.POST['identidad']) | Q(nombre=request.POST['identidad'])).filter(pestana=6)[:1].get()
			else:
				cliente = Clientes.objects.filter(Q(identidad=request.POST['identidad']) | Q(cliente_interno=request.POST['identidad']) | Q(nombre=request.POST['identidad']))[:1].get()
			url = '/cobranzas/gestion/'+str(cliente.cliente)
			ctx = {
				'cliente' : cliente,
				'url' : url,
				'gestiones' : gestiones
			}
		except Exception as e:
			ctx = {
				'mensaje' : 'error',
				'gestiones' : gestiones
			}

	return render(request, 'buscar_agente.html', ctx)


#Enviar el correo electronico con el historial de pago
@login_required()
def enviar_correo(request):
	if request.is_ajax():
		final = False
		if request.GET.get('metodo') == 'plan_pago':
			id = request.GET['credito']

			from django.db import connection
			cursor = connection.cursor()
			#Traer el historial del credito seleccionado
			try:
				query = "SELECT * FROM [CCCOB].[fnGetPlanPagoCliente]('%s') ORDER BY CONVERT(DATE, fecha, 105) ASC"%id
				cursor.execute(query)
				data = dictfetchall(cursor)
			except Exception as e:
				print e
				data = False
				pass
			finally:
				cursor.close()

			#Si se realizo bien la consulta se procede a enviar el correo
			if data:
				import smtplib
				from email.mime.multipart import MIMEMultipart
				from email.mime.text import MIMEText

				email_from = 'Soporte@banrural.com.hn'
				email_to = request.GET['correo']
				msg = MIMEMultipart('alternative')
				msg['Subject'] = 'Plan de Pago - Credito N. ' + request.GET['credito']
				msg['From'] = email_from
				msg['To'] = email_to

				body = request.GET['mensaje']
				body += "<br><br>"
				body += "<b>Plan de Pago para el Credito N.  %s</b>"%request.GET['credito']
				body += "<br>"
				
				body += "<table style='border-collapse:collapse;border-spacing:0;'>"
				body += "<tr>"
				body += "<tr>"
				body += "<th style='padding:10px 5px; border-style:solid;border-width:1px;overflow:hidden;word-break:normal;' >FECHA</th>"
				body += "<th style='padding:10px 5px; border-style:solid;border-width:1px;overflow:hidden;word-break:normal;' >CUOTA</th>"
				body += "<th style='padding:10px 5px; border-style:solid;border-width:1px;overflow:hidden;word-break:normal;' >CAPITAL</th>"
				body += "<th style='padding:10px 5px; border-style:solid;border-width:1px;overflow:hidden;word-break:normal;' >INTERESES</th>"
				body += "</tr>"

				for registro in data:
					body += "<tr>"
					body += "<td style = 'padding:8px 5px; border-style:solid;border-width:1px;overflow:hidden;word-break:normal;' >{0}</td>".format(registro['fecha'])
					body += "<td style = 'padding:8px 5px; border-style:solid;border-width:1px;overflow:hidden;word-break:normal;' >{0}</td>".format(registro['cuota'])
					body += "<td style = 'padding:8px 5px; border-style:solid;border-width:1px;overflow:hidden;word-break:normal;' >{0}</td>".format(registro['capital'] )
					body += "<td style = 'padding:8px 5px; border-style:solid;border-width:1px;overflow:hidden;word-break:normal;' >{0}</td>".format(registro['intereses'])
					body += "</tr>"
				body += "<br>"

				msg.attach(MIMEText(body.encode('utf-8'), 'html', 'utf-8'))

				# Credentials (if needed)
				#username = '900007@banrural.com.hn'
				#password = 'Temporal32k'

				# The actual mail send
				server = smtplib.SMTP('192.168.1.50:25')
				#server.starttls()
				#server.login(username,password)
				#server.sendmail(fromaddr, toaddrs + toaddrs2 , msg.as_string())
				server.sendmail(email_from, email_to, msg.as_string())
				server.quit()
				final = True

		return HttpResponse(json.dumps(final), content_type='application/json')

@login_required()
def gestiones_por_dia(request):
	date_object = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
	gestiones_por_dia = ClientesGestiones.objects.filter(fecha_gestion=datetime.date.today(), agente=request.user)
	ctx = {'gestiones_por_dia':gestiones_por_dia,'numeroClientes':gestiones_por_dia.count()}

	return render(request, 'gestiones_por_dia.html', ctx)


@login_required()
def buscar_toda_informacion_cliente(request):
	#Llama el metodo de las gestiones
	gestiones = obtener_gestiones(request.user.id)
	ctx = {'gestiones':gestiones}
	if request.POST:
		try:
			cliente = Clientes.objects.filter(Q(identidad=request.POST['identidad']) | Q(cliente_interno=request.POST['identidad']) | Q(nombre=request.POST['identidad'])).order_by('fecha_actualizado_merge')[:1].get()
			ctx = {
				'cliente' : cliente,
				'gestiones' : gestiones
			}
		except Exception as e:
			print e
			ctx = {
				'mensaje' : 'error',
				'gestiones' : gestiones
			}
	return render(request, 'buscar_toda_informacion_cliente.html', ctx)

@login_required()
def sucursales(request):
	#Gestiones del cliente
	gestiones = obtener_gestiones(request.user.id)
	totales = obtener_mora(request.user.id, 6)
	request.session['url'] = '/cobranzasbo/gestionesbo/'
	request.session['pagina_principal'] = '/cobranzas/sucursales/'

	try:
		del request.session['cuentas']
		del request.session['creditos']
		del request.session['pagos']
		del request.session['gestiones_cliente']
		del request.session['transacciones_tarjetas']
		del request.session['promesa_pago']
		del request.session['referencias']
	except Exception as e:
		pass

	fecha = datetime.datetime.today()
	#Recordatorios
	gest= ClientesGestiones.objects.filter(resultado_gestion=3, agente=request.user, cliente__pestana=6)
	recordatorios = []
	for gestion in gest:
		if fecha >= gestion.devolver_llamada:
			recordatorios.append({'cliente': gestion.cliente.nombre , 'fecha': gestion.devolver_llamada.strftime('%Y-%m-%d %I:%M:%S%p')})

	if request.is_ajax():
		id = request.GET['id']

		try:
			#AQUI PONE EN SESION TODAS LOS DETALLES DEL CLIENTE
			from django.db import connection
			cursor = connection.cursor()

			persona = dict(
				Clientes.objects.values(
					'cliente',
					'nombre',
					'sexo',
					'correo_electronico',
					'identidad',
					'cant_creditos',
					'saldo_total_creditos',
					'capital_mora',
					'intereses_mora',
					'intereses_moratorios',
					'otros_recargos',
					'dias_atraso',
					'cuotas_mora'
				).get(cliente_interno=id)
			)
			gestiones = list(
				ClientesGestiones.objects.values(
					'telefono',
					'tipo_gestion'
				).filter(cliente=persona['cliente'])
			)

			
			#Traer la Informacion General de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetInformacionGeneral](%s)"%id
				cursor.execute(query)
				persona = dictfetchall(cursor)
				request.session['persona'] = persona
				print persona , '-------------------------------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PASO POR AQUI'
			except Exception as e:
				print e
				persona = False

			#Traer las CUENTAS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetCuentasCliente](%s)"%id
				cursor.execute(query)
				cuentas = dictfetchall(cursor)
				request.session['cuentas'] = cuentas
				request.session['lacuenta'] = float(request.session['cuentas'][0]['saldo'].replace(',',''))
			except Exception as e:
				cuentas = False


			#Traer los CREDITOS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetCreditosCliente](%s)"%id
				cursor.execute(query)
				creditos = dictfetchall(cursor)
				request.session['creditos'] = creditos
				print query
			except Exception as e:
				print e
				creditos = False

			#Traer los TRANSACCIONES DE TARJETAS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetTransaccionesTarjetasCliente](%s)"%id
				cursor.execute(query)
				transacciones_tarjetas = dictfetchall(cursor)
				request.session['transacciones_tarjetas'] = transacciones_tarjetas
				#print transacciones_tarjetas
			except Exception as e:
				print e
				transacciones_tarjetas = False


			#Traer los PAGOS de los clientes
			try:
				query = "SELECT * FROM [CCCOB].[fnGetPagosCliente](%s) ORDER BY CONVERT(DATE, fecha, 105) DESC"%id
				cursor.execute(query)
				pagos = dictfetchall(cursor)
				request.session['pagos'] = pagos
				#print pagos
			except Exception as e:
				print e
				pagos = False
			finally:
				cursor.close()

			try:
				request.session['gestiones_cliente'] = gestiones_cliente = list(ClientesGestiones.objects.filter(cliente=id).extra({'inicio': "CONVERT(varchar(15), FechaInicio, 111)", 'final': "CONVERT(varchar(15), FechaFinal, 111)", 'hora_inicio': "CONVERT(varchar(15), FechaInicio, 108)", 'hora_final': "CONVERT(varchar(15), FechaFinal, 108)"}).values('tipo_gestion__descripcion', 'resultado_gestion__descripcion', 'telefono__telefono', 'agente__username', 'inicio', 'final', 'hora_inicio', 'hora_final'))
			except Exception as e:
				gestiones_cliente = False
				pass

		except Exception, e:
			print e
			persona = False
			gestiones = False
			cuentas = False
			creditos = False
			transacciones_tarjetas = False
			pagos = False
			gestiones_cliente = False


		data = {
			'gestiones': gestiones,
			'gestiones_cliente': gestiones_cliente,
			'persona': persona, #[{str(row) : val} for row, val in persona]
			'cuentas' : cuentas,
			'creditos' : creditos,
			'transacciones_tarjetas' : transacciones_tarjetas,
			'pagos' : pagos,
		}

		return HttpResponse(json.dumps(data, default=decimal_default), content_type='application/json')
	if request.method == 'GET':
		clientes = Clientes.objects.filter(agente=request.user, capital_mora__gte=1, pestana=6, hoy_actualizado=False, tiene_promesa = False, status=True)
		mora = Clientes.objects.filter(agente=request.user, capital_mora__lte=1, dias_atraso__lte=1, pestana=6, hoy_actualizado=False, tiene_promesa = False, status=True)
		clientes_castigados = Clientes.objects.filter(agente=request.user, capital_mora=0, dias_atraso__gte=1, pestana=6, hoy_actualizado=False, tiene_promesa = False, status=True)
		clientes_pendientes = ClientesGestiones.objects.filter(resultado_gestion=3, agente=request.user, cliente__pestana=6).extra({'fecha_cast': "CAST(DevolverLlamada as DATE)"}).order_by('fecha_cast')[:15]
		clientes_promesa = ClientesPromesas.objects.filter(cliente__pestana=6, cliente__agente=request.user, estado='PENDIENTE', fecha__gte=datetime.date.today()).exclude(cod_gestion__fecha_gestion=datetime.date.today())

		ctx={
			'clientes': clientes,
			'mora': mora,
			'clientes_pendientes': clientes_pendientes,
			'clientes_promesa': clientes_promesa,
			'clientes_castigados': clientes_castigados,
			'gestiones': gestiones,
			'hoy':datetime.date.today(),
			'promesa': ClientesPromesas.objects.filter(cliente__pestana=6, cliente__agente=request.user, estado='PENDIENTE', fecha=datetime.date.today()).exclude(cod_gestion__fecha_gestion=datetime.date.today()).count(),
			'recordatorios':recordatorios,
			'totales': totales,
		}
	return render(request, 'sucursales.html', ctx)


@login_required()
def mensaje_masivo(request):
	clientes = Clientes.objects.filter(agente=request.user)
	ctx = { 'clientes': clientes }
	if request.POST:
		clientes = request.POST.getlist('cliente')
		for pk in clientes:
			cliente = Clientes.objects.get(pk=pk)
			telefonos = ClientesTelefono.objects.filter(cliente=cliente, mensaje=True)

			from django.db import connection
			import time
			with connection.cursor() as cursor:
				for telefono in telefonos:
					cursor.execute("EXEC [ADSYSPROC\SQL2008].SMSServer.dbo.InsertSMSFromCRM @MessageTo='+504%s', @MessageFrom = 'BANRURAL', @MessageText ='%s'"%( telefono.telefono , request.POST['mensaje'] ))
					cursor.execute("SELECT 1 ")
					row = cursor.fetchone()

					gestion = ClientesGestiones()
					gestion.cliente = cliente
					gestion.cliente_interno = cliente.cliente_interno

					gestion.tipo_gestion = TiposGestion.objects.get(tipo_gestion = 2) #Mensaje
					gestion.resultado_gestion = ResultadoGestion.objects.get(resultado_gestion=9) #Mensaje
					
					gestion.observaciones = 'MENSAJE MASIVO'
					gestion.mensaje = request.POST.get('mensaje')
					gestion.telefono = telefono
					gestion.fecha_inicio = datetime.datetime.today()
					gestion.agente = request.user
					gestion.fecha_gestion =  time.strftime("%Y-%m-%d")
					gestion.save()

					ctx = { 'clientes': Clientes.objects.filter(agente=request.user) , 'exito': True }
	return render(request, 'mensaje_masivo.html', ctx)


@login_required()
def nota_cobro_masivo(request, cantidad):
	if int(cantidad) <= 29:
		clientes = Clientes.objects.filter(agente=request.user, dias_atraso__lte=30, cuotas_mora__gte=1)
	elif int(cantidad) >= 30 and int(cantidad) <= 59:
		clientes = Clientes.objects.filter(agente=request.user, dias_atraso__gte=30, dias_atraso__lte=59, cuotas_mora__gte=1)
	elif int(cantidad) >= 60 and int(cantidad) <= 89:
		clientes = Clientes.objects.filter(agente=request.user, dias_atraso__gte=60, dias_atraso__lte=89, cuotas_mora__gte=1)
	elif int(cantidad) >= 90:
		clientes = Clientes.objects.filter(agente=request.user, dias_atraso__gte=90, cuotas_mora__gte=1)

	ctx = { 'clientes': clientes, 'cantidad':cantidad }
	if request.POST:
		clientes = request.POST.getlist('cliente')
		for pk in clientes:
			cliente = Clientes.objects.get(pk=pk)
			telefonos = ClientesTelefono.objects.filter(cliente=cliente, mensaje=True)

			from django.db import connection
			import time
			with connection.cursor() as cursor:
				for telefono in telefonos:
					cursor.execute("EXEC [ADSYSPROC\SQL2008].SMSServer.dbo.InsertSMSFromCRM @MessageTo='+504%s', @MessageFrom = 'BANRURAL', @MessageText ='%s'"%( telefono.telefono , request.POST['mensaje'] ))
					cursor.execute("SELECT 1 ")
					row = cursor.fetchone()

					gestion = ClientesGestiones()
					gestion.cliente = cliente
					gestion.cliente_interno = cliente.cliente_interno

					gestion.tipo_gestion = TiposGestion.objects.get(tipo_gestion = 2) #Mensaje
					gestion.resultado_gestion = ResultadoGestion.objects.get(resultado_gestion=9) #Mensaje
					
					gestion.observaciones = 'MENSAJE MASIVO'
					gestion.mensaje = request.POST.get('mensaje')
					gestion.telefono = telefono
					gestion.fecha_inicio = datetime.datetime.today()
					gestion.agente = request.user
					gestion.fecha_gestion =  time.strftime("%Y-%m-%d")
					gestion.save()

					ctx = { 'clientes': Clientes.objects.filter(agente=request.user) , 'exito': True }
	return render(request, 'nota_cobro_masivo.html', ctx)

#Menu donde se selecciona el tipo de nota de cobro que se quiere generar
@login_required()
def menu_nota_cobro(request):
	request.session['url'] = '/menu/nota_cobro/'

	ctx = {}
	return render(request, 'menu_nota_cobro.html', ctx)




@login_required()
def carga_callcenter(request):
	mensaje = False
	formulario = AsignacionCarteraForm()

	if request.POST:
		from django.db import connection, transaction
		cursor = connection.cursor()
		
		if request.POST['cartera'] == '1':
			#Ejecuta la Bancon
			try:
				query = "EXECUTE [dbo].[CargarBancon] @mora_inicio=%s, @mora_final = %s  "%(request.POST['mora_desde'], request.POST['mora_hasta'])
				cursor.execute(query)
				row = cursor.fetchall()
				transaction.commit()
				mensaje = 'exito'
			except Exception as e:
				raise e
				mensaje = 'error'
			finally:
				cursor.close()

		if request.POST['cartera'] == '2':
			#Ejecuta la Banrural
			try:
				query = "EXECUTE [dbo].[CargarBanrural] @mora_inicio=%s, @mora_final = %s  "%(request.POST['mora_desde'], request.POST['mora_hasta'])
				cursor.execute(query)
				row = cursor.fetchall()
				transaction.commit()
				mensaje = 'exito'
			except Exception as e:
				mensaje = 'error'
			finally:
				cursor.close()

		if request.POST['cartera'] == '3':
			#Ejecuta la Premora
			try:
				query = "EXECUTE [dbo].[CargarPremora] @fecha_pago = '%s'  "%request.POST['fecha']
				cursor.execute(query)
				row = cursor.fetchall()
				transaction.commit()
				mensaje = 'exito'
			except Exception as e:
				mensaje = 'error'
			finally:
				cursor.close()

	ctx = {
		'mensaje': mensaje,
		'formulario': formulario
		}

	return render(request, 'carga_callcenter.html', ctx)



@login_required()
def asignacion_cartera(request, gestor):
	formulario = AsignacionCarteraForm()
	gestor = User.objects.get(pk=gestor)

	ctx = {
		'formulario': formulario,
		'gestor': gestor,
		'clientes': Clientes.objects.filter(pestana=5, agente__isnull=True)
	}


	if request.POST:
		query = {}
		query['pestana'] = 5
		query['agente__isnull'] = True
		if request.POST.getlist('producto') == [] and request.POST.getlist('agencia') == [] and request.POST.get('desde_mora') == '' and request.POST.get('hasta_mora') == '' and request.POST.get('desde_capital') == '' and request.POST.get('hasta_capital') == '':
			pass
		else:
			query['producto_credito__in'] = ProductosCredito.objects.values_list('nombre_corto', flat=True).all() if request.POST.getlist('producto') == [] else ProductosCredito.objects.values_list('nombre_corto', flat=True).filter(pk__in=request.POST.getlist('producto'))
			query['agencia__in'] = Agencias.objects.values_list('pk', flat=True).all() if request.POST.getlist('agencia') == [] else request.POST.getlist('agencia')
			query['dias_atraso__gte'] = 0 if request.POST.get('desde_mora') == '' or request.POST.get('desde_mora') == None else  request.POST.get('desde_mora')
			query['dias_atraso__lte'] = 100000000000000 if request.POST.get('hasta_mora') == '' or request.POST.get('hasta_mora') == None else  request.POST.get('hasta_mora')
			query['saldo_total_creditos__gte'] =  0 if request.POST.get('desde_capital') == '' or request.POST.get('desde_capital') == None else  request.POST.get('desde_capital') 
			query['saldo_total_creditos__lte'] =  1000000000000 if  request.POST.get('hasta_capital') == '' or request.POST.get('hasta_capital') == None else   request.POST.get('hasta_capital')

		clientes = Clientes.objects.filter(**query)
		formulario = AsignacionCarteraForm(request.POST)
		#print clientes.query
		
		if request.POST['metodo'] == 'buscar':

			ctx = {
				'formulario': formulario,
				'gestor': gestor,
				'clientes' : clientes
			}
		elif request.POST['metodo'] == 'asignar':
			if request.POST.getlist('producto') == []:
				productos = 'Todos los productos' 
			else:
				productos = [str(num) for num in ProductosCredito.objects.values_list('nombre_corto', flat=True).filter(pk__in=request.POST.getlist('producto')) ]
				productos = ', '.join(productos) 

			if request.POST.getlist('agencia') == []:
				agencias = 'Todos las agencias' 
			else:
				agencias = [str(num) for num in Agencias.objects.values_list('nombre_agencia', flat=True).filter(pk__in=request.POST.getlist('agencia')) ]
				agencias = ', '.join(agencias) 

			if request.POST.get('todo') == 'on':

				historial = HistorialAsignacion()
				historial.productos =  productos
				historial.agencias = agencias
				historial.dias_mora = request.POST.get('desde_mora', ' ') + ' - ' + request.POST.get('hasta_mora', ' ')
				historial.capital_mora = request.POST.get('desde_capital', ' ') + ' - ' + request.POST.get('hasta_capital', ' ')
				historial.agente = gestor
				historial.estado = 1
				historial.save()

				clientes.update(agente = gestor)
			else:

				clientes_guardar = request.POST.getlist('cliente')

				historial = HistorialAsignacion()
				historial.productos =  productos
				historial.agencias = agencias
				historial.dias_mora = request.POST.get('desde_mora', ' ') + ' - ' + request.POST.get('hasta_mora', ' ')
				historial.capital_mora = request.POST.get('desde_capital', ' ') + ' - ' + request.POST.get('hasta_capital', ' ')
				historial.agente = gestor
				historial.estado = 1
				historial.save()
 
				Clientes.objects.filter(pk__in= clientes_guardar).update(agente = gestor)



			ctx = {
				'formulario': formulario,
				'gestor': gestor,
				'mensaje': 'exito',
				'clientes' : clientes
				#'clientes' : clientes
			}

	return render(request, 'asignacion_cartera.html', ctx)


@login_required()
def listado_gestores(request):
	gestores = User.objects.filter(groups__name__contains='BO')
	historiales = HistorialAsignacion.objects.filter(estado = True)

	gstor = []
	for gestor in gestores:
		nose = {}
		nose['pk'] = gestor.pk
		nose['username'] = gestor.username
		nose['last_name'] = gestor.last_name
		nose['first_name'] = gestor.first_name
		dic = []
		for historial in historiales:
			if historial.agente.pk == gestor.pk:
				algo = {}
				algo['cod_historial'] = historial.cod_historial
				algo['productos'] = historial.productos
				algo['agencias'] = historial.agencias
				algo['dias_mora'] = historial.dias_mora
				algo['capital_mora'] = historial.capital_mora
				algo['fecha'] = historial.fecha

				dic.append(algo)

		
		nose['historial'] = dic

		gstor.append(nose)


	ctx = {
		'gestores': gstor,
		#'historial' : historial
	}

	return render(request, 'listado_gestores.html', ctx)


@login_required()
def desasignacion_cartera(request, codigo):
	historial = HistorialAsignacion.objects.get(cod_historial=codigo)
	historial.estado = 0
	historial.save()
	return HttpResponseRedirect(reverse('listado_gestores'))

