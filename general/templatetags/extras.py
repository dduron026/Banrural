
from django.contrib.auth.models import Group 
from django import template

#obtener el grupo que pertenece 
register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    group =  Group.objects.filter(name__contains=group_name) 
    statement = False
    for g in group:
    	statement = g in user.groups.all() 
    	if statement == True:
    		return True
    return False