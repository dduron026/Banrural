from django.contrib import admin
from reclamos.models import *

# class AgentesAdmin(admin.ModelAdmin):
#     #list_display = ('question_text', 'pub_date', 'was_published_recently')
#     search_fields = ['nombre']

admin.site.register(Estados)
admin.site.register(TipoAcciones)
admin.site.register(Categorias)
admin.site.register(TiposReclamo)
admin.site.register(Reclamos)
admin.site.register(Acciones)





