from django.contrib import admin
from .models import Tutor

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('get_nombre_completo', 'email', 'telefono', 'fecha_registro')
    search_fields = ('nombre', 'apellido', 'email', 'telefono')
    list_filter = ('fecha_registro',)
    ordering = ('apellido', 'nombre')