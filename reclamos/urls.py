from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.reclamo, name='reclamo'),
	url(r'^listado/$', views.listado_reclamos, name='listado_reclamos'),

	url(r'^cuenta/paso/uno/(?P<cat>[0-9]+)/(?P<rec>[0-9]+)/(?P<id>[0-9]+)$', views.cuenta_paso_uno, name='cuenta_paso_uno'),
	url(r'^cuenta/paso/dos/(?P<cat>[0-9]+)/(?P<rec>[0-9]+)/(?P<id>[0-9]+)/(?P<cuenta>[0-9]+)$', views.cuenta_paso_dos, name='cuenta_paso_dos'),
	url(r'^cuenta/paso/tres/(?P<cat>[0-9]+)/(?P<rec>[0-9]+)/(?P<id>[0-9]+)/(?P<cuenta>[0-9]+)$', views.cuenta_paso_tres, name='cuenta_paso_tres'),


	url(r'^prestamo/paso/uno/(?P<cat>[0-9]+)/(?P<rec>[0-9]+)/(?P<id>[0-9]+)$', views.prestamo_paso_uno, name='prestamo_paso_uno'),
	url(r'^prestamo/paso/dos/(?P<cat>[0-9]+)/(?P<rec>[0-9]+)/(?P<id>[0-9]+)/(?P<cuenta>[0-9]+)$', views.prestamo_paso_dos, name='prestamo_paso_dos'),
	url(r'^prestamo/paso/tres/(?P<cat>[0-9]+)/(?P<rec>[0-9]+)/(?P<id>[0-9]+)/(?P<cuenta>[0-9]+)$', views.prestamo_paso_tres, name='prestamo_paso_tres'),
]