from django.conf.urls import url
from . import views

urlpatterns = [
	#COBRANZASBO
	url(r'^$', views.listado_clientes, name='listado_clientes'),
	url(r'^gestionesbo/(?P<id>[0-9]+)$', views.gestionesbo, name='gestionesbo'),
	url(r'^visita/(?P<id>[0-9]+)$', views.visita, name='visita'),

	#Aqui va el listado de los telefonos, es una vista generica
	url(r'^gestion_cliente/(?P<id>[0-9]+)$', views.gestion_cliente, name='gestion_cliente'),
	#---------------------------------------------
	url(r'^pre_judicial/(?P<id>[0-9]+)$', views.pre_judicial, name='pre_judicial'),
	url(r'^judicial/(?P<id>[0-9]+)$', views.judicial, name='judicial'),
	url(r'^visita/(?P<id>[0-9]+)/(?P<direccion>.+)/$', views.visita, name='visita'),
	url(r'^nota_cobro/(?P<id>[0-9]+)$', views.nota_cobro, name='nota_cobro'),
	url(r'^correo/(?P<id>[0-9]+)$', views.correo, name='correo'),
	url(r'^direcciones/nota_cobro/(?P<id>[0-9]+)$', views.direcciones_nota_cobro, name='direcciones_nota_cobro'),
	
]