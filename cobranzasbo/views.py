# -*- coding: utf-8 -*-
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
from cobranzas.views import obtener_gestiones
from cobranzas.views import gestiones_por_dia


import time
import datetime
import json
import decimal


def date_handler(obj):
	if hasattr(obj, 'isoformat'):
		return obj.isoformat()
	else:
		raise TypeError

@login_required()
def listado_clientes(request):
	#Gestiones del cliente
	gestiones = obtener_gestiones(request.user.id)
	request.session['url'] = '/cobranzasbo/gestionesbo/'
	request.session['pagina_principal'] = '/cobranzasbo/'

	fecha = datetime.datetime.today()
	#Recordatorios
	gest= ClientesGestiones.objects.filter(resultado_gestion=3, agente=request.user, cliente__pestana=1)
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
			referencias = False


		data = {
			'gestiones': gestiones,
			'gestiones_cliente': gestiones_cliente,
			'persona': persona, 
			'cuentas' : cuentas,
			'creditos' : creditos,
			'referencias' : referencias,
			'transacciones_tarjetas' : transacciones_tarjetas,
			'pagos' : pagos,
		}

		return HttpResponse(json.dumps(data, default=decimal_default), content_type='application/json')
	if request.method == 'GET':
		#clientes = Clientes.objects.filter(agente=request.user, pestana=1, saldo_total_creditos__gte=0, hoy_actualizado=False, tiene_promesa = False)
		clientes = Clientes.objects.filter(pestana=1, saldo_total_creditos__gte=0, hoy_actualizado=False, tiene_promesa = False)[:250]
		clientes_castigados = Clientes.objects.filter(pestana=1, agente=request.user, capital_mora=0, dias_atraso__gte=1, hoy_actualizado=False, tiene_promesa = False, status=True)
		clientes_pendientes = ClientesGestiones.objects.filter(cliente__pestana=1,resultado_gestion=3, agente=request.user).extra({'fecha_cast': "CAST(DevolverLlamada as DATE)"}).order_by('fecha_cast')[:15]
		clientes_promesa = ClientesPromesas.objects.filter(cliente__pestana=1, cliente__agente=request.user, estado='PENDIENTE', fecha__gte=datetime.date.today()).exclude(cod_gestion__fecha_gestion=datetime.date.today())

		formulario = ClienteActualizarForm()
		formulario2 = ClienteHistoricoForm()
		ctx={
			'formulario': formulario,
			'formulario2': formulario2,
			'clientes': clientes,
			'clientes_pendientes': clientes_pendientes,
			'clientes_castigados': clientes_castigados,
			'clientes_promesa': clientes_promesa,
			'gestiones': gestiones,
			'hoy':datetime.date.today(),
			'promesa': ClientesPromesas.objects.filter(cliente__pestana=1, cliente__agente=request.user, estado='PENDIENTE', fecha=datetime.date.today()).exclude(cod_gestion__fecha_gestion=datetime.date.today()).count(),
			'recordatorios':recordatorios,
			'numeroClientes':clientes.count()
			
		}
		return render(request, 'listado_clientes.html', ctx)

#Menu donde se selecciona la opcion que se desea con el cliente
@login_required()
def gestionesbo(request, id):
	request.session['url'] = '/cobranzasbo/gestionesbo/'+id

	cliente =  Clientes.objects.get(cliente= id)	
	ctx={
		'cliente_id' : id,
		'cliente':cliente
	}

	return render(request, 'gestionesbo.html', ctx)

#Pantalla donde sale los numeros de telefonos del cliente que se selecciono
@login_required()
@transaction.atomic
def gestion_cliente(request, id):

	if request.POST:
		#Si el cliente contesta normal
		date_object = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
		
		if request.POST['metodo'] == 'direccion':
			from distutils.util import strtobool
			try:
				with transaction.atomic():

					# codireccion = models.AutoField(db_column='CodDireccion', primary_key=True)  # Field name made lowercase.
					# cliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='CodCliente')  # Field name made lowercase.
					# tipo_direcciones = models.ForeignKey('Tiposdirecciones', models.DO_NOTHING, db_column='CodTipoDirecciones', blank=True, null=True)  # Field name made lowercase.
					# departamento = models.ForeignKey('Departamentos', models.DO_NOTHING, db_column='CodDepartamento', blank=True, null=True)  # Field name made lowercase.
					# municipio = models.ForeignKey('Municipios', models.DO_NOTHING, db_column='CodMunicipio', blank=True, null=True)  # Field name made lowercase.
					# colonia = models.ForeignKey('Colonias', models.DO_NOTHING, db_column='CodColonia', blank=True, null=True)  # Field name made lowercase.
					# direccion = models.CharField(db_column='Direccion', max_length=200)  # Field name made lowercase.
					# activo = models.NullBooleanField(db_column='Activo')  # Field name made lowercase.
					
					gestion = ClientesDirecciones()
					gestion.cliente = Clientes.objects.get(cliente=id)
					try:
						gestion.tipo_direcciones = TiposDirecciones.objects.get(tipo_direcciones=request.POST['tipo_direccion'])
					except Exception as e:
						gestion.tipo_direcciones = None
						pass

					try:
						gestion.departamento = Departamentos.objects.get(codigo=request.POST['departamento'])
						
					except Exception as e:
						gestion.departamento = None
						
					
					try:
						gestion.municipio = Municipios.objects.get(municipio=request.POST['municipio'])
						
					except Exception as e:
						gestion.municipio = None
						

					try:
						gestion.colonia = Colonias.objects.get(colonia=request.POST['colonia'])
					except Exception as e:
						gestion.colonia = None

					try:
						gestion.direccion = request.POST['direccion']
					except Exception as e:
						gestion.direccion = None

					try:
						gestion.activo = True
					except Exception as e:
						gestion.activo = None
						
					gestion.save()

					cliente =  Clientes.objects.get(cliente= id)
					tipo_direccion = TiposDirecciones.objects.all()
					departamentos = Departamentos.objects.values(
					'codigo',
					'descripcion'
					)
					
					
			except Exception as e:
				raise e
				mensaje = 'error'
	elif request.is_ajax():
		tabla = request.GET['tabla']
		valor = request.GET['valor']
		if tabla == 'municipio':
			data = list(Municipios.objects.values('municipio', 'descripcion').filter(departamento=valor))
		elif tabla == 'colonia':
			data = list(Colonias.objects.values( 'colonia', 'descripcion').filter(municipio=valor))
		return HttpResponse(json.dumps(data, default=date_handler), content_type='application/json')

	cliente =  Clientes.objects.get(cliente= id)
	tipos_direcciones = TiposDirecciones.objects.all()
	departamentos = Departamentos.objects.all()
	direcciones = ClientesDirecciones.objects.values(
		'codireccion',
		'direccion',
		'tipo_direcciones__descripcion'
	).filter(cliente=id)

	ctx={
		'cliente': cliente,
		'direcciones': direcciones,
		'departamentos': departamentos,
		'tipos_direcciones': tipos_direcciones

	}
	return render(request, 'gestion_cliente.html', ctx)


#Pantalla donde se registra la visita del cliente
@login_required()
@transaction.atomic
def visita(request, id, direccion):
	cliente =  Clientes.objects.get(cliente= id)

	if request.POST:
		#Si el cliente contesta normal
		date_object = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
		if request.POST['metodo'] == 'localizado':
			#Se eliminan los pendientes anteriores, si existe
			try:
				with transaction.atomic():
					gestion = ClientesGestiones()
					gestion.cliente = Clientes.objects.get(cliente=id)
					gestion.cliente_interno = Clientes.objects.get(cliente=id).cliente_interno
					gestion.tipo_gestion = TiposGestion.objects.get(tipo_gestion = 3) #CAMBIAR DESPUES
					gestion.resultado_gestion = ResultadoGestion.objects.get(resultado_gestion=4) #VISITA
					gestion.observaciones = request.POST['observaciones']
					gestion.razon = request.POST['opcion']
					gestion.direccion=direccion


					gestion.fecha_inicio = date_object
					gestion.agente = request.user

					gestion.save()

				return HttpResponseRedirect(reverse('listado_clientes'))
			except Exception as e:
				raise e
				mensaje = 'error'
		
		elif request.POST['metodo'] == 'direccion':
			from distutils.util import strtobool
			try:
				with transaction.atomic():

					
					
					gestion = ClientesDirecciones()
					gestion.cliente = Clientes.objects.get(cliente=id)
					try:
						gestion.tipo_direcciones = TiposDirecciones.objects.get(tipo_direcciones=request.POST['tipo_direccion'])
					except Exception as e:
						gestion.tipo_direcciones = None
						pass

					try:
						gestion.departamento = Departamentos.objects.get(codigo=request.POST['departamento'])
						
					except Exception as e:
						gestion.departamento = None
						
					
					try:
						gestion.municipio = Municipios.objects.get(municipio=request.POST['municipio'])
						
					except Exception as e:
						gestion.municipio = None
						

					try:
						gestion.colonia = Colonias.objects.get(colonia=request.POST['colonia'])
					except Exception as e:
						gestion.colonia = None

					try:
						gestion.direccion = request.POST['direccion']
					except Exception as e:
						gestion.direccion = None

					try:
						gestion.activo = True
					except Exception as e:
						gestion.activo = None
						
					gestion.save()

					cliente =  Clientes.objects.get(cliente= id)
					tipo_direccion = TiposDirecciones.objects.all()
					departamentos = Departamentos.objects.values(
					'codigo',
					'descripcion'
					)
					
					
			except Exception as e:
				raise e
				mensaje = 'error'

	elif request.is_ajax():
		tabla = request.GET['tabla']
		print "----------------------------",tabla
		valor = request.GET['valor']
		print "----------------------------",valor
		if tabla == 'municipio':
			data = list(Municipios.objects.values('municipio', 'descripcion').filter(departamento=valor))
		elif tabla == 'colonia':
			data = list(Colonias.objects.values( 'colonia', 'descripcion').filter(municipio=valor))
		return HttpResponse(json.dumps(data, default=date_handler), content_type='application/json')
	
	else:
		cliente =  Clientes.objects.get(cliente= id)
		tipo_direccion = TiposDirecciones.objects.all()

		departamentos = Departamentos.objects.values(
		'codigo',
		'descripcion'
		)
	

	ctx={
		'cliente': cliente,
		'tipo_direccion':tipo_direccion,
		'departamentos':departamentos,
	}
	return render(request, 'visita.html', ctx)


#Pantalla donde se manda el correo a los clientes
@login_required()
@transaction.atomic
def correo(request, id):
	cliente =  Clientes.objects.get(cliente= id)
	if request.POST:
		#Si el cliente contesta normal
		date_object = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
		#Se eliminan los pendientes anteriores, si existe
		try:
			with transaction.atomic():
				gestion = ClientesGestiones()
				gestion.cliente = Clientes.objects.get(cliente=id)
				gestion.cliente_interno = Clientes.objects.get(cliente=id).cliente_interno
				gestion.tipo_gestion = TiposGestion.objects.get(tipo_gestion = 24) #CAMBIAR DESPUES 
				gestion.resultado_gestion = ResultadoGestion.objects.get(resultado_gestion=8) #ENVIAR CORREO
				gestion.correo = request.POST['correo']
				gestion.titulo_mensaje = request.POST['titulo']
				gestion.mensaje = request.POST['mensaje']
				gestion.observaciones = "Se envio correo a: " + request.POST['correo']


				gestion.fecha_inicio = date_object
				gestion.agente = request.user

				gestion.save()

				import smtplib
				from email.mime.multipart import MIMEMultipart
				from email.mime.text import MIMEText

				email_from = 'Soporte@banrural.com.hn'
				email_to = request.POST['correo']
				msg = MIMEMultipart('alternative')
				msg['Subject'] = request.POST['titulo']
				msg['From'] = email_from
				msg['To'] = email_to

				body = request.POST['mensaje']
				msg.attach(MIMEText(body.encode('utf-8'), 'html', 'utf-8'))

				# Credentials (if needed)
				#username = '900007@banrural.com.hn'
				#password = 'Temporal32h'

				# The actual mail send
				
				server = smtplib.SMTP('192.168.1.50:25')
				#server = smtplib.SMTP('smtp.office365.com:587')
				#server.starttls()
				#server.login(username,password)
				#server.sendmail(fromaddr, toaddrs + toaddrs2 , msg.as_string())
				server.sendmail(email_from, email_to, msg.as_string())
				server.quit()


			return HttpResponseRedirect(reverse('listado_clientes'))
		except Exception as e:
			raise e
			mensaje = 'error'
	else:
		cliente =  Clientes.objects.get(cliente= id)
	

	ctx={
		'cliente': cliente,
	}
	return render(request, 'correo.html', ctx)


#Pantalla donde se traslada el cliente a Judicial
@login_required()
@transaction.atomic
def judicial(request, id):
	cliente =  Clientes.objects.get(cliente= id)
	bufetes = Bufetes.objects.values('bufete', 'descripcion').all()

	if request.POST:
		#Si el cliente contesta normal
		date_object = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
		try:
			with transaction.atomic():
				gestion = ClientesGestiones()
				gestion.cliente = Clientes.objects.get(cliente=id)
				gestion.cliente_interno = Clientes.objects.get(cliente=id).cliente_interno
				gestion.tipo_gestion = TiposGestion.objects.get(tipo_gestion = 10) #CAMBIAR DESPUES
				gestion.resultado_gestion = ResultadoGestion.objects.get(resultado_gestion=7) #VISITA
				gestion.observaciones = request.POST['observaciones']
				gestion.bufete = request.POST['bufete']
				gestion.adjunto = request.FILES['adjunto']

				gestion.fecha_inicio = date_object
				gestion.agente = request.user

				gestion.save()

			return HttpResponseRedirect(reverse('listado_clientes'))
			#return HttpResponseRedirect(reverse('judicial', kwargs={'id':id}))
		except Exception as e:
			raise e
			mensaje = 'error'
		
	else:
		cliente =  Clientes.objects.get(cliente= id)
	

	ctx={
		'cliente': cliente,
		'bufetes': bufetes,
	}
	return render(request, 'judicial.html', ctx)


#Pantalla donde se traslada el cliente a prejudicial
@login_required()
@transaction.atomic
def pre_judicial(request, id):
	cliente =  Clientes.objects.get(cliente= id)

	if request.POST:
		#Si el cliente contesta normal
		date_object = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
		try:
			with transaction.atomic():
				gestion = ClientesGestiones()
				gestion.cliente = Clientes.objects.get(cliente=id)
				gestion.cliente_interno = Clientes.objects.get(cliente=id).cliente_interno
				gestion.tipo_gestion = TiposGestion.objects.get(tipo_gestion = 10) #CAMBIAR DESPUES
				gestion.resultado_gestion = ResultadoGestion.objects.get(resultado_gestion=6) #VISITA
				gestion.observaciones = request.POST['observaciones']
				gestion.adjunto = request.FILES['adjunto']

				gestion.fecha_inicio = date_object
				gestion.agente = request.user

				gestion.save()

			return HttpResponseRedirect(reverse('listado_clientes'))
			#return HttpResponseRedirect(reverse('judicial', kwargs={'id':id}))
		except Exception as e:
			raise e
			mensaje = 'error'
		
	else:
		cliente =  Clientes.objects.get(cliente= id)
	

	ctx={
		'cliente': cliente,
	}
	return render(request, 'pre_judicial.html', ctx)


#Pantalla donde se registra la visita del cliente
@login_required()
@transaction.atomic
def nota_cobro(request, id):
	cliente =  Clientes.objects.get(cliente= id)
	direcciones = ClientesDirecciones.objects.values(
		'codireccion',
		'tipo_direcciones__descripcion',
		'direccion',
	).filter(cliente=id)

	try:
		agente = Agentes.objects.get(usuario=request.user)
	except Exception as e:
		agente = {}

	if request.POST:
		#Si el cliente contesta normal
		date_object = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
		if request.POST['metodo'] == 'localizado':
			#Se eliminan los pendientes anteriores, si existe
			try:
				with transaction.atomic():
					gestion = ClientesGestiones()
					gestion.cliente = Clientes.objects.get(cliente=id)
					gestion.cliente_interno = Clientes.objects.get(cliente=id).cliente_interno
					gestion.tipo_gestion = TiposGestion.objects.get(tipo_gestion = 3) #CAMBIAR DESPUES
					gestion.resultado_gestion = ResultadoGestion.objects.get(resultado_gestion=5) #VISITA
					gestion.direccion = request.POST.get('direccion')
					
					gestion.nombre_tercero = request.POST['nombre']
					gestion.razon = request.POST['opcion']
					gestion.observaciones = request.POST['observaciones']
					gestion.monto_promesa = request.POST.get('monto_promesa')

					gestion.fecha_inicio = date_object
					gestion.agente = request.user

					gestion.save()

					direccion = ClientesDirecciones.objects.get(pk=request.POST.get('direccion'))
				return redirect()

				return HttpResponseRedirect(reverse('listado_clientes'))
			except Exception as e:
				raise e
				mensaje = 'error'
		
		elif request.POST['metodo'] == 'direccion':
			from distutils.util import strtobool
			try:
				with transaction.atomic():
					gestion = ClientesDirecciones()
					gestion.cliente = Clientes.objects.get(cliente=id)
					try:
						gestion.tipo_direcciones = TiposDirecciones.objects.get(tipo_direcciones=request.POST['tipo_direccion'])
					except Exception as e:
						gestion.tipo_direcciones = None
						pass

					try:
						gestion.departamento = Departamentos.objects.get(codigo=request.POST['departamento'])
						
					except Exception as e:
						gestion.departamento = None
						
					
					try:
						gestion.municipio = Municipios.objects.get(municipio=request.POST['municipio'])
						
					except Exception as e:
						gestion.municipio = None
						

					try:
						gestion.colonia = Colonias.objects.get(colonia=request.POST['colonia'])
					except Exception as e:
						gestion.colonia = None

					try:
						gestion.direccion = request.POST['direccion']
					except Exception as e:
						gestion.direccion = None

					try:
						gestion.activo = True
					except Exception as e:
						gestion.activo = None
						
					gestion.save()

					cliente =  Clientes.objects.get(cliente= id)
					tipo_direccion = TiposDirecciones.objects.all()
					departamentos = Departamentos.objects.values(
					'codigo',
					'descripcion'
					)
					
					
			except Exception as e:
				raise e
				mensaje = 'error'

	elif request.is_ajax():
		tabla = request.GET['tabla']
		valor = request.GET['valor']
		if tabla == 'municipio':
			data = list(Municipios.objects.values('municipio', 'descripcion').filter(departamento=valor))
		elif tabla == 'colonia':
			data = list(Colonias.objects.values( 'colonia', 'descripcion').filter(municipio=valor))
		return HttpResponse(json.dumps(data, default=date_handler), content_type='application/json')
	
	else:
		cliente =  Clientes.objects.get(cliente= id)
		tipo_direccion = TiposDirecciones.objects.all()
		departamentos = Departamentos.objects.all()
	

	ctx={
		'cliente': cliente,
		'tipo_direccion':tipo_direccion,
		'departamentos':departamentos,
		'direcciones':direcciones,
	}
	return render(request, 'nota_cobro.html', ctx)




#Pantalla donde sale las direcciones de los clientes y que iran a la nota de cobro
@login_required()
@transaction.atomic
def direcciones_nota_cobro(request, id):

	if request.POST:
		#Si el cliente contesta normal
		date_object = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
		
		if request.POST['metodo'] == 'direccion':
			from distutils.util import strtobool
			try:
				with transaction.atomic():

					gestion = ClientesDirecciones()
					gestion.cliente = Clientes.objects.get(cliente=id)
					try:
						gestion.tipo_direcciones = TiposDirecciones.objects.get(tipo_direcciones=request.POST['tipo_direccion'])
					except Exception as e:
						gestion.tipo_direcciones = None
						pass

					try:
						gestion.departamento = Departamentos.objects.get(codigo=request.POST['departamento'])
						
					except Exception as e:
						gestion.departamento = None
						
					
					try:
						gestion.municipio = Municipios.objects.get(municipio=request.POST['municipio'])
						
					except Exception as e:
						gestion.municipio = None
						

					try:
						gestion.colonia = Colonias.objects.get(colonia=request.POST['colonia'])
					except Exception as e:
						gestion.colonia = None

					try:
						gestion.direccion = request.POST['direccion']
					except Exception as e:
						gestion.direccion = None

					try:
						gestion.activo = True
					except Exception as e:
						gestion.activo = None
						
					gestion.save()

					cliente =  Clientes.objects.get(cliente= id)
					tipo_direccion = TiposDirecciones.objects.all()
					departamentos = Departamentos.objects.values(
					'codigo',
					'descripcion'
					)
					
					
			except Exception as e:
				raise e
				mensaje = 'error'
	elif request.is_ajax():
		tabla = request.GET['tabla']
		valor = request.GET['valor']
		if tabla == 'municipio':
			data = list(Municipios.objects.values('municipio', 'descripcion').filter(departamento=valor))
		elif tabla == 'colonia':
			data = list(Colonias.objects.values( 'colonia', 'descripcion').filter(municipio=valor))
		return HttpResponse(json.dumps(data, default=date_handler), content_type='application/json')

	cliente =  Clientes.objects.get(cliente= id)
	tipos_direcciones = TiposDirecciones.objects.all()
	departamentos = Departamentos.objects.all()
	direcciones = ClientesDirecciones.objects.values(
		'codireccion',
		'direccion',
		'tipo_direcciones__descripcion'
	).filter(cliente=id)

	import locale
	locale.setlocale(locale.LC_ALL, 'esp_esp')
	fecha = datetime.date.today()
	hoy = fecha.strftime("%A %d de %B del %Y") 

	try:
		agente = Agentes.objects.get(usuario=request.user)
	except Exception as e:
		agente = {}

	# nota_cobro = 'http://dwhsrv/reports/report/Notas%20de%20Cobro/Nota%20de%20Cobro%20-%2015%20dias?fecha=%s&direccion=%s&nombre_cliente=%s&credito=%s&saldo=%s&usuario=%s'%(fecha, cliente.direccion, cliente.nombre, cliente.credito, cliente.saldo_total_creditos, agente.nombre)

	ctx={
		'cliente': cliente,
		'direcciones': direcciones,
		'departamentos': departamentos,
		'tipos_direcciones': tipos_direcciones,
		'hoy': hoy.decode('ISO-8859-1'),
		'agente': agente

	}
	return render(request, 'direcciones_nota_cobro.html', ctx)

