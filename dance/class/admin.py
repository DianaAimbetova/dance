from django.contrib import admin
from .models import Class

# Register your models here.
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created']