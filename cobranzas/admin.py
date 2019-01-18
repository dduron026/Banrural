from django.contrib import admin
from cobranzas.models import *

class ClientesAdmin(admin.ModelAdmin):
    #list_display = ('question_text', 'pub_date', 'was_published_recently')
    search_fields = ['nombre']


class AgentesAdmin(admin.ModelAdmin):
    #list_display = ('question_text', 'pub_date', 'was_published_recently')
    search_fields = ['nombre']

admin.site.register(Clientes, ClientesAdmin)
admin.site.register(ClientesDirecciones)
admin.site.register(ClientesGestiones)
admin.site.register(ClientesTelefono)
admin.site.register(Departamentos)
admin.site.register(Municipios)
admin.site.register(ResultadoGestion)
admin.site.register(TiposDirecciones)
admin.site.register(TiposEstados)
admin.site.register(TiposGestion)
admin.site.register(TiposPestanas)
admin.site.register(TiposTelefonos)
admin.site.register(Agentes, AgentesAdmin)