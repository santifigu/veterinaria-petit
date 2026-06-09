from django.contrib import admin
from django.utils.html import format_html
from .models import Veterinario


@admin.register(Veterinario)
class VeterinarioAdmin(admin.ModelAdmin):
    list_display = ('foto_thumb', 'get_nombre_completo', 'matricula', 'especialidad', 'telefono', 'consultas_realizadas', 'activo')
    list_filter = ('activo', 'especialidad')
    search_fields = ('nombre', 'apellido', 'matricula', 'email')
    list_editable = ('activo',)
    raw_id_fields = ('user',)

    def foto_thumb(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="width:36px;height:36px;border-radius:50%;object-fit:cover;"/>', obj.foto.url)
        return format_html('<div style="width:36px;height:36px;border-radius:50%;background:#e8f5e9;display:flex;align-items:center;justify-content:center;">👨‍⚕️</div>')
    foto_thumb.short_description = ''

    def consultas_realizadas(self, obj):
        from mascota.models import HistorialMedico
        cantidad = HistorialMedico.objects.filter(veterinario=obj).count()
        if cantidad == 0:
            return '—'
        return format_html(
            '<a href="/admin/mascota/historialmedico/?veterinario__id={}">{} consulta{}</a>',
            obj.id, cantidad, 's' if cantidad != 1 else ''
        )
    consultas_realizadas.short_description = 'Consultas'