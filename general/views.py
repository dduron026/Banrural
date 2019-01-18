# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import *
from django.template import RequestContext
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers  import make_password
from django.contrib.auth.models import User, Group
from django.db import transaction, IntegrityError
from banrural.settings import EN_SERVIDOR
from general.models import *
from banrural.settings import EN_SERVIDOR
import json
import decimal
from django.db.models import Count
from cobranzas.models import ClientesGestiones



#Convertir los decimales en formato que el JSON pueda reconocerlo
def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)

#Convertir en diccionarios los cursores [{campo : valor1, campo2: valor2}]
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

import ldap
def auth(username, password):
    conn = ldap.initialize('ldap://192.168.1.11:389')
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    try:
        result = conn.simple_bind_s('GFBanruralHN\\'+username, password)
    except ldap.INVALID_CREDENTIALS:
        return "Invalid credentials"
    except ldap.SERVER_DOWN:
        return "Server down"
    except ldap.LDAPError, e:
        if type(e.message) == dict and e.message.has_key('desc'):
            return "Other LDAP error: " + e.message['desc']
        else: 
            return "Other LDAP error: " + e
    finally:
        conn.unbind_s()
    return True


def cerrar_sesion(request):
	if request.POST:
		try:
			with transaction.atomic():
				import datetime
				manejo_sesion = Logueos()
				manejo_sesion.usuarioid = User.objects.get(username=request.user.username)
				hora = datetime.datetime.now()
				hora = hora.strftime("%Y-%m-%d %H:%M:%S")

				manejo_sesion.hora = hora
				manejo_sesion.estado = 0
				manejo_sesion.motivo = request.POST['motivo']
				manejo_sesion.observaciones = request.POST['observaciones']
				manejo_sesion.save()

		except Exception as e:
			raise e
		logout(request)
		return redirect('login')	
	else:
		ctx={}
		return render(request, 'logout.html', ctx)

@transaction.atomic
def login(request):
	ctx = {}
	logout(request)
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		if EN_SERVIDOR==True:
			active_directory = auth(username, password)
			if active_directory == True:
				try:
					user = User.objects.get(username = username)
					user.set_password(password)
					user.save()
				except Exception as e:
					pass
			else:
				pass

		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				auth_login(request, user)
				try:
					with transaction.atomic():
						import datetime
						manejo_sesion = Logueos()
							
						manejo_sesion.usuarioid = User.objects.get(username=username)
						
						hora = datetime.datetime.now()
						hora = hora.strftime("%Y-%m-%d %H:%M:%S")

						manejo_sesion.hora = hora
						manejo_sesion.estado = 1
						manejo_sesion.save()

				except Exception as e:
					raise e
				return HttpResponseRedirect(reverse('menu'))
			else:
				ctx = {
					'error': True,
					'username': username,
				}
		else:
			ctx = {
				'error': True,
				'username': username,
			}
	return render(request, 'login.html', ctx)

@login_required()
def menu(request):

	
	#sirve para agarrar los clientes y enviarlos para informacion importante.
	clientes = list(ClientesGestiones.objects.values('agente__first_name').filter(tipo_gestion=2).annotate(alias=(Count('tipo_gestion'))))
	#clientes = [{str(k): str(v) for k, v in elem.items()} for elem in clientes]
	ctx={'clientes':clientes}
	return render(request, 'principal.html', ctx)

@login_required()
def usuarios(request):
	grupos = Group.objects.all()
	mensaje = ''

	if request.POST:
		username = request.POST['usuario']
		grupo = request.POST['grupo']
		try:
			User.objects.get(username=username)
			mensaje = 'error'
		except Exception as e:
			usuario = User()
			usuario.username = username
			usuario.is_staff = False
			usuario.save()

			g = Group.objects.get(id=grupo) 
			g.user_set.add(usuario)
			mensaje = 'exito'

			print mensaje, 'asdlkasldkjsal'

	ctx={ 'grupos': grupos, 'mensaje': mensaje  }
	return render(request, 'usuarios.html', ctx)


#Pantalla donde el cliente es localizado y responde las preguntas
@login_required()
def ajax_general(request):
	data = {}
	from django.db import connection
	cursor = connection.cursor()
	if request.GET['opcion'] == 'busqueda_usuario':
		id = request.GET['usuario']
		#Traer el historial del credito seleccionado
		try:
			query = "SELECT * FROM [CCCOB].[fnGetUser]('%s')"%id
			cursor.execute(query)
			data = dictfetchall(cursor)
		except Exception as e:
			data = e
			pass
		finally:
			cursor.close()

	return HttpResponse(json.dumps(data, default=decimal_default), content_type='application/json')
