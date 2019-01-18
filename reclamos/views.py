# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import *
from django.template import RequestContext
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.db.models import Count, CharField, Case, Value, When, Sum, IntegerField, Q
from django.db import connection
from django.utils import timezone
from reclamos.models import *
from cobranzas.models import Agencias

import json

@login_required()
def reclamos(request):
	ctx={}
	return render(request, 'reclamos.html', ctx)

#Convertir en diccionarios los cursores [{campo : valor1, campo2: valor2}]
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0].decode('utf8') for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@login_required()
def reclamo(request):
	if request.is_ajax():
		if request.GET['metodo'] == 'categoria':
			try:
				data = list(TiposReclamo.objects.values().filter(categoria__pk=request.GET['codigo']))
			except Exception as e:
				data = {}
		elif request.GET['metodo'] == 'buscar_identidad':
			#Se abre una conexion a la base de datos
			from django.db import connection
			cursor = connection.cursor()
			
			#Traer la Informacion General de los clientes
			try:
				query = "SELECT * FROM [Rec].[fnGetCliente] ('%s') "%request.GET['identidad']
				cursor.execute(query)
				persona = dictfetchall(cursor)
				request.session['persona'] = persona
				data = persona
			except Exception as e:
				data = {}
			finally:
				cursor.close()
		return HttpResponse(json.dumps(data), content_type='application/json')
		
	elif request.POST:
		print request.POST['categoria'], 'NOSE'
		if request.POST['categoria'] in ('5','6'):
			categoria = Categorias.objects.get(pk=request.POST['categoria'])

			reclamo =  Reclamos()
			reclamo.cliente = request.session['persona'][0]['cliente_interno']
			reclamo.identidad = request.session['persona'][0]['identidad']
			reclamo.categoria = categoria
			#reclamo.tipo_reclamo = tipo_reclamo
			reclamo.observaciones = request.POST['reclamo']
			reclamo.oficial_ingresa = request.user.pk
			reclamo.save()

			import smtplib
			from email.mime.multipart import MIMEMultipart
			from email.mime.text import MIMEText

			email_from = 'ReclamosCRM@banrural.com.hn'
			email_to = request.POST['correo']
			msg = MIMEMultipart('alternative')
			msg['Subject'] = 'Ingreso de Reclamo N. ' + str(reclamo.reclamo)
			msg['From'] = email_from
			msg['To'] = email_to

			body = '<b> Estimado (a): </b>' + request.session['persona'][0]['nombre'] + '<br><br>'
			body += 'Se ha registrado con exito su reclamo para su seguimiento: <br><br>'
			body += '<b> Tipo de Reclamo: </b> ' + categoria.nombre + '<br>'
			#body += '<b> N. Transaccion: </b>' + request.session['transaccion'][0]  +'<br>' #+ ' / ' + request.session['transaccion'][1] +'<br>'
			body += '<b> Detalle de Reclamo: </b> <br>' + request.POST['reclamo'] + '<br>'
			body += '<br><br><br> Nuestra mision es ayudarle en todo lo posible. Proximamente estara recibiendo el seguimiento de su reclamo.'


			msg.attach(MIMEText(body.encode('utf-8'), 'html', 'utf-8'))
			server = smtplib.SMTP('192.168.1.50:25')
			server.sendmail(email_from, email_to, msg.as_string())
			server.quit()

			return HttpResponseRedirect(reverse('reclamo'))
		elif request.POST['categoria'] == '1':
			return HttpResponseRedirect(reverse('cuenta_paso_uno', args=[ request.POST['categoria'], request.POST['tipo_reclamo'], request.POST['cliente'] ]))
		elif request.POST['categoria'] == '3':
			return HttpResponseRedirect(reverse('prestamo_paso_uno', args=[ request.POST['categoria'], request.POST['tipo_reclamo'], request.POST['cliente'] ]))
		else:
			return HttpResponseRedirect(reverse('cuenta_paso_uno', args=[ request.POST['categoria'], request.POST['tipo_reclamo'], request.POST['cliente'] ]))
	else:
		categorias = Categorias.objects.all()
	ctx={	
		'categorias': categorias,
		'sucursales': Agencias.objects.all()

	}
	return render(request, 'reclamo.html', ctx)

@login_required()
def cuenta_paso_uno(request, cat, rec, id):
	if request.POST:
		return HttpResponseRedirect(reverse('cuenta_paso_dos', args=[ cat, rec, id, request.POST['cuenta'] ]))
	else:

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
		finally:
			cursor.close()

		ctx={
		'cuentas':cuentas
		}

		return render(request, 'cuenta/paso_uno.html', ctx)



@login_required()
def cuenta_paso_dos(request, cat, rec, id, cuenta):
	from django.db import connection
	cursor = connection.cursor()

	if request.POST:
		if request.POST['metodo'] == 'filtro':
			try:
				query = "SELECT * FROM [Rec].[fnGetTransaccionesCliente]('%s','%s','%s')"%(cuenta, request.POST['desde'], request.POST['hasta'])
				print query
				cursor.execute(query)
				transacciones = dictfetchall(cursor)
				request.session['transacciones'] = transacciones
			except Exception as e:
				transacciones = False
			finally:
				cursor.close()
			ctx={
				'transacciones':transacciones,
				'desde':request.POST['desde'], 
				'hasta':request.POST['hasta'],
				'categoria': cat,
				'reclamo': rec,
				'id': id
			}
		else:
			request.session['transaccion'] = request.POST.getlist('transaccion')
			return HttpResponseRedirect(reverse('cuenta_paso_tres', args=[ cat, rec, id, cuenta ]))

	else:
		try:
			query = "SELECT * FROM [Rec].[fnGetTransaccionesCliente]('%s','','')"%cuenta
			cursor.execute(query)
			transacciones = dictfetchall(cursor)
			request.session['transacciones'] = transacciones
		except Exception as e:
			transacciones = False
		finally:
			cursor.close()

		ctx={
			'transacciones':transacciones,
			'categoria': cat,
			'reclamo': rec,
			'id': id
		}

	return render(request, 'cuenta/paso_dos.html', ctx)



@login_required()
def cuenta_paso_tres(request, cat, rec, id, cuenta):
	from django.db import connection
	cursor = connection.cursor()

	try:
		query = "SELECT * FROM [Rec].[fnGetTransaccionesCliente]('%s','','')"%cuenta
		cursor.execute(query)
		transacciones = dictfetchall(cursor)
		request.session['transacciones'] = transacciones
	except Exception as e:
		transacciones = False
	finally:
		cursor.close()

	ctx={
		'transacciones':transacciones,
		'categoria': cat,
		'reclamo': rec,
		'id': id,
		'cuenta' : cuenta
	}

	if request.POST:
		categoria = Categorias.objects.get(pk=cat)
		tipo_reclamo = TiposReclamo.objects.get(pk=rec)

		reclamo =  Reclamos()
		reclamo.cliente = request.session['persona'][0]['cliente_interno']
		reclamo.identidad = request.session['persona'][0]['identidad']
		reclamo.categoria = categoria
		reclamo.tipo_reclamo = tipo_reclamo
		reclamo.ref1 = cuenta
		# reclamo.ref2 = 
		# reclamo.ref3 = 
		# reclamo.ref4 = 
		reclamo.observaciones = request.POST['reclamo']
		reclamo.oficial_ingresa = request.user.pk
		reclamo.save()


		import smtplib
		from email.mime.multipart import MIMEMultipart
		from email.mime.text import MIMEText

		email_from = 'ReclamosCRM@banrural.com.hn'
		email_to = request.POST['correo']
		msg = MIMEMultipart('alternative')
		msg['Subject'] = 'Ingreso de Reclamo N. ' + str(reclamo.reclamo)
		msg['From'] = email_from
		msg['To'] = email_to

		body = '<b> Estimado (a): </b>' + request.session['persona'][0]['nombre'] + '<br><br>'
		body += 'Se ha registrado con exito su reclamo para su seguimiento: <br><br>'
		body += '<b> Tipo de Reclamo: </b> ' + categoria.nombre + '<br>'
		body += '<b> N. Transaccion: </b>' + request.session['transaccion'][0]  +'<br>' #+ ' / ' + request.session['transaccion'][1] +'<br>'
		body += '<b> Detalle de Reclamo: </b> <br>' + request.POST['reclamo'] + '<br>'
		body += '<br><br><br> Nuestra mision es ayudarle en todo lo posible. Proximamente estara recibiendo el seguimiento de su reclamo.'

		#request.POST['reclamo']
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

		return HttpResponseRedirect(reverse('reclamo'))


	return render(request, 'cuenta/paso_tres.html', ctx)



@login_required()
def prestamo_paso_uno(request, cat, rec, id):
	if request.POST:
		return HttpResponseRedirect(reverse('prestamo_paso_dos', args=[ cat, rec, id, request.POST['prestamo'] ]))
	else:
		from django.db import connection
		cursor = connection.cursor()
		#Traer las CUENTAS de los clientes
		try:
			query = "SELECT * FROM [CCCOB].[fnGetCreditosCliente](%s)"%id
			cursor.execute(query)
			prestamos = dictfetchall(cursor)
			request.session['prestamos'] = prestamos
		except Exception as e:
			prestamos = False
		finally:
			cursor.close()

		ctx={
		'prestamos':prestamos
		}

		return render(request, 'prestamo/paso_uno.html', ctx)


@login_required()
def prestamo_paso_dos(request, cat, rec, id, cuenta):
	from django.db import connection
	cursor = connection.cursor()

	if request.POST:
		if request.POST['metodo'] == 'filtro':
			try:
				query = "SELECT * FROM [CCCOB].[fnGetHistorialPagoCliente]('%s','%s','%s')"%(cuenta, request.POST['desde'], request.POST['hasta'])
				cursor.execute(query)
				transacciones = dictfetchall(cursor)
				request.session['transacciones'] = transacciones
			except Exception as e:
				transacciones = False
			finally:
				cursor.close()
			ctx={
				'transacciones':transacciones,
				'desde':request.POST['desde'], 
				'hasta':request.POST['hasta'],
				'categoria': cat,
				'reclamo': rec,
				'id': id
			}
		else:
			request.session['transaccion'] = request.POST.getlist('transaccion')
			print request.POST.getlist('transaccion') , 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
			return HttpResponseRedirect(reverse('prestamo_paso_tres', args=[ cat, rec, id, cuenta ]))

	else:
		try:
			query = "SELECT * FROM [CCCOB].[fnGetHistorialPagoCliente]('%s')"%cuenta
			cursor.execute(query)
			transacciones = dictfetchall(cursor)
			request.session['transacciones'] = transacciones
		except Exception as e:
			transacciones = False
		finally:
			cursor.close()

		ctx={
			'transacciones':transacciones,
			'categoria': cat,
			'reclamo': rec,
			'id': id
		}

	return render(request, 'prestamo/paso_dos.html', ctx)



@login_required()
def prestamo_paso_tres(request, cat, rec, id, cuenta):
	from django.db import connection
	cursor = connection.cursor()

	try:
		query = "SELECT * FROM [Rec].[fnGetTransaccionesCliente]('%s','','')"%cuenta
		cursor.execute(query)
		transacciones = dictfetchall(cursor)
		request.session['transacciones'] = transacciones
	except Exception as e:
		transacciones = False
	finally:
		cursor.close()

	ctx={
		'transacciones':transacciones,
		'categoria': cat,
		'reclamo': rec,
		'id': id,
		'cuenta' : cuenta
	}

	if request.POST:
		categoria = Categorias.objects.get(pk=cat)
		tipo_reclamo = TiposReclamo.objects.get(pk=rec)

		reclamo =  Reclamos()
		reclamo.cliente = request.session['persona'][0]['cliente_interno']
		reclamo.identidad = request.session['persona'][0]['identidad']
		reclamo.categoria = categoria
		reclamo.tipo_reclamo = tipo_reclamo
		#reclamo.ref1 = cuenta
		reclamo.ref2 = cuenta
		# reclamo.ref3 = 
		# reclamo.ref4 = 
		reclamo.observaciones = request.POST['reclamo']
		reclamo.oficial_ingresa = request.user.pk
		reclamo.save()


		import smtplib
		from email.mime.multipart import MIMEMultipart
		from email.mime.text import MIMEText

		email_from = 'ReclamosCRM@banrural.com.hn'
		email_to = request.POST['correo']
		msg = MIMEMultipart('alternative')
		msg['Subject'] = 'Ingreso de Reclamo N. ' + str(reclamo.reclamo)
		msg['From'] = email_from
		msg['To'] = email_to

		body = '<b> Estimado (a): </b>' + request.session['persona'][0]['nombre'] + '<br><br>'
		body += 'Se ha registrado con exito su reclamo para su seguimiento: <br><br>'
		body += '<b> Tipo de Reclamo: </b> ' + categoria.nombre + '<br>'
		body += '<b> N. Transaccion: </b>' + request.session['transaccion'][0]  +'<br>' #+ ' / ' + request.session['transaccion'][1] +'<br>'
		body += '<b> Detalle de Reclamo: </b> <br>' + request.POST['reclamo'] + '<br>'
		body += '<br><br><br> Nuestra mision es ayudarle en todo lo posible. Proximamente estara recibiendo el seguimiento de su reclamo.'

		#request.POST['reclamo']
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

		return HttpResponseRedirect(reverse('reclamo'))


	return render(request, 'prestamo/paso_tres.html', ctx)


@login_required()
def listado_reclamos(request):
	reclamos = Reclamos.objects.filter(oficial_ingresa=request.user.pk)
	#reclamos = [{str(k): str(v) for k, v in elem.items()} for elem in reclamos]
	ctx={'reclamos':reclamos}
	return render(request, 'listado_reclamos.html', ctx)
