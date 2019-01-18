from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.login, name='login'),
	url(r'^accounts/login/$', views.login, name='login'),
	url(r'^logout/$', views.cerrar_sesion, name='cerrar_sesion'),
	url(r'^menu/$', views.menu, name='menu'),
	url(r'^usuarios/$', views.usuarios, name='usuarios'),
	url(r'^ajax/general/$', views.ajax_general, name='ajax_general'),
]