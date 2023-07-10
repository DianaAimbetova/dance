from operator import ge
from django import template
from ..models import Class

register = template.Library() 

@register.filter(name='has_enrolled') 
def has_enrolled(user, class_id):
    return Class.objects.filter(id=class_id, students__in=[user]).exists() 