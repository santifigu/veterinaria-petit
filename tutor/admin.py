from django.contrib import admin
from django.utils.html import format_html
from .models import Tutor


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('get_nombre_completo', 'email', 'telefono', 'ver_mascotas', 'fecha_registro')
    search_fields = ('nombre', 'apellido', 'email', 'telefono')
    list_filter = ('fecha_registro',)
    ordering = ('apellido', 'nombre')
    raw_id_fields = ('tutor',)

    def ver_mascotas(self, obj):
        cantidad = obj.mascotas.count()
        if cantidad == 0:
            return '—'
        return format_html(
            '<a href="/admin/mascota/mascota/?tutor__id={}">{} mascota{}</a>',
            obj.id, cantidad, 's' if cantidad != 1 else ''
        )
    ver_mascotas.short_description = 'Mascotas'