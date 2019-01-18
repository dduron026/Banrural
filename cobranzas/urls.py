from django.conf.urls import url
from . import views

urlpatterns = [
	#COBRANZAS
	url(r'^$', views.morosidad_primera_cuota, name='morosidad_primera_cuota'),
	url(r'^banrural/$', views.opcion2, name='opcion2'),
	url(r'^pre_mora/$', views.opcion3, name='opcion3'),
	url(r'^gestion/(?P<id>[0-9]+)$', views.gestion, name='gestion'),
	url(r'^gestion/llamar/(?P<id>[0-9]+)/(?P<tel>.+)/$', views.gestion_llamar, name='gestion_llamar'),
	url(r'^gestion/localizado/(?P<id>[0-9]+)/(?P<tel>.+)/$', views.gestion_localizado, name='gestion_localizado'),
	url(r'^gestion/ajax$', views.gestion_ajax, name='gestion_ajax'),
	url(r'^buscar/gestionados/$', views.buscar_gestionados, name='buscar_gestionados'),
	url(r'^buscar/agente$', views.buscar_agente, name='buscar_agente'),
	url(r'^enviar/correo/$', views.enviar_correo, name='enviar_correo'),
	url(r'^gestiones/por_dia/$', views.gestiones_por_dia, name='gestiones_por_dia'),
	url(r'^buscar/informacion_cliente/$', views.buscar_toda_informacion_cliente, name='buscar_toda_informacion_cliente'),
	

	#SUCURSALES
	url(r'^sucursales/$', views.sucursales, name='sucursales'),
	url(r'^mensaje/masivo/$', views.mensaje_masivo, name='mensaje_masivo'),
	url(r'^nota_cobro/masivo/(?P<cantidad>[0-9]+)$', views.nota_cobro_masivo, name='nota_cobro_masivo'),
	url(r'^menu/nota_cobro/$', views.menu_nota_cobro, name='menu_nota_cobro'),

	#Supervisor
	url(r'^carga/callcenter$', views.carga_callcenter, name='carga_callcenter'),
	url(r'^asignacion/cartera/(?P<gestor>[0-9]+)$', views.asignacion_cartera, name='asignacion_cartera'),
	url(r'^desasignacion/cartera/(?P<codigo>[0-9]+)$', views.desasignacion_cartera, name='desasignacion_cartera'),
	url(r'^listado/gestores$', views.listado_gestores, name='listado_gestores'),

]