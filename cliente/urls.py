from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.actualizar_callcenter, name='actualizar_callcenter'),
	url(r'^ajax/$', views.ajax, name='ajax'),
	url(r'^reporte/operadores$', views.reporte_operadores, name='reporte_operadores'),
	url(r'^reporte/clientes$', views.reporte_clientes, name='reporte_clientes'),
	url(r'^actualizar/$', views.actualizar_cliente, name='actualizar_cliente'),
	url(r'^revision/calidad/$', views.revision_calidad, name='revision_calidad'),
	url(r'^busqueda/ticket/$', views.busqueda_ticket, name='busqueda_ticket'),
	url(r'^modificar/$', views.modificar_cliente, name='modificar_cliente'),

	#COBRANZAS
	#url(r'^cobranza/morosidad/primera_cuota$', views.morosidad_primera_cuota, name='morosidad_primera_cuota'),
	url(r'^prospectacion/prestamos/fiduciarios$', views.prestamos_fiduciarios, name='prestamos_fiduciarios'),

]