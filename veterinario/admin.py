from django.contrib import admin
from .models import Veterinario

@admin.register(Veterinario)
class VeterinarioAdmin(admin.ModelAdmin):
    list_display = ('get_nombre_completo', 'matricula', 'especialidad', 'telefono', 'activo')
    list_filter = ('activo', 'especialidad')
    search_fields = ('nombre', 'apellido', 'matricula', 'email')
    list_editable = ('activo',)
    raw_id_fields = ('user',)