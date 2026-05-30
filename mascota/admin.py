from django.contrib import admin
from django.utils.html import format_html
from .models import Mascota, RegistroVacunacion, HistorialMedico, Archivo, ControlAntiparasitario


# ══ INLINES ══

class RegistroVacunacionInline(admin.TabularInline):
    model = RegistroVacunacion
    extra = 1
    fields = ['nombre_vacuna', 'fecha_aplicacion', 'proxima_dosis', 'veterinario', 'lote', 'laboratorio', 'observaciones']
    autocomplete_fields = ['veterinario']
    verbose_name = "Vacuna"
    verbose_name_plural = "📋 Registro de Vacunación"


class ControlAntiparasitarioInline(admin.TabularInline):
    model = ControlAntiparasitario
    extra = 1
    fields = ['fecha', 'antiparasitario', 'peso_en_fecha', 'proxima_desparasitacion', 'veterinario', 'observaciones']
    autocomplete_fields = ['veterinario']
    verbose_name = "Control"
    verbose_name_plural = "🐛 Control Antiparasitario"


class HistorialMedicoInline(admin.StackedInline):
    model = HistorialMedico
    extra = 0
    fields = ['tipo', 'fecha', 'veterinario', 'motivo_consulta', 'diagnostico', 'tratamiento', 'medicamentos', 'peso', 'temperatura', 'proxima_visita', 'observaciones']
    autocomplete_fields = ['veterinario']
    verbose_name = "Consulta"
    verbose_name_plural = "🏥 Historial Médico"
    show_change_link = True  # link para ver el detalle completo


class ArchivoInline(admin.TabularInline):
    model = Archivo
    extra = 0
    fields = ['tipo', 'titulo', 'archivo', 'fecha', 'descripcion']
    verbose_name = "Archivo"
    verbose_name_plural = "📁 Archivos (Rx, análisis, ecografías)"


# ══ MASCOTA ADMIN ══

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('foto_thumbnail', 'nombre', 'tipo', 'raza', 'tutor', 'peso', 'estado_badge', 'microchip', 'activo')
    list_filter = ('tipo', 'sexo', 'activo')
    search_fields = ('nombre', 'tutor__nombre', 'tutor__apellido', 'microchip')
    raw_id_fields = ('tutor',)
    list_editable = ('activo',)
    readonly_fields = ('fecha_registro', 'foto_preview', 'get_edad')

    fieldsets = (
        ('🐾 Datos de la Mascota', {
            'fields': ('tutor', 'nombre', 'tipo', 'raza', 'sexo', 'fecha_nacimiento', 'get_edad', 'color', 'microchip', 'activo')
        }),
        ('📊 Estado y Medidas', {
            'fields': ('estado', 'peso', 'altura', 'foto', 'foto_preview')
        }),
        ('📝 Observaciones', {
            'fields': ('observaciones', 'fecha_registro'),
            'classes': ('collapse',)
        }),
    )

    inlines = [
        RegistroVacunacionInline,
        ControlAntiparasitarioInline,
        HistorialMedicoInline,
        ArchivoInline,
    ]

    def foto_thumbnail(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="width:40px;height:40px;border-radius:8px;object-fit:cover;"/>', obj.foto.url)
        return format_html('<div style="width:40px;height:40px;border-radius:8px;background:#e8f5e9;display:flex;align-items:center;justify-content:center;font-size:18px;">🐾</div>')
    foto_thumbnail.short_description = ''

    def foto_preview(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="width:120px;height:120px;border-radius:16px;object-fit:cover;"/>', obj.foto.url)
        return "Sin foto"
    foto_preview.short_description = 'Vista previa'

    def get_edad(self, obj):
        edad = obj.get_edad()
        return f"{edad} año{'s' if edad != 1 else ''}" if edad is not None else "—"
    get_edad.short_description = 'Edad'

    def estado_badge(self, obj):
        colores = {
            'saludable': ('#22c55e', '✅ Saludable'),
            'chequeo':   ('#f59e0b', '⚠️ Chequeo'),
            'critico':   ('#ef4444', '🚨 Crítico'),
        }
        color, label = colores.get(obj.estado, ('#6b7280', obj.estado))
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">{}</span>',
            color, label
        )
    estado_badge.short_description = 'Estado'


# ══ REGISTROS INDIVIDUALES (para búsqueda directa) ══

@admin.register(RegistroVacunacion)
class RegistroVacunacionAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'nombre_vacuna', 'fecha_aplicacion', 'proxima_dosis', 'veterinario', 'lote')
    list_filter = ('fecha_aplicacion', 'veterinario')
    search_fields = ('mascota__nombre', 'nombre_vacuna', 'lote')
    date_hierarchy = 'fecha_aplicacion'
    raw_id_fields = ('mascota', 'veterinario')


@admin.register(ControlAntiparasitario)
class ControlAntiparasitarioAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'antiparasitario', 'fecha', 'peso_en_fecha', 'proxima_desparasitacion', 'veterinario')
    list_filter = ('fecha', 'veterinario')
    search_fields = ('mascota__nombre', 'antiparasitario')
    date_hierarchy = 'fecha'
    raw_id_fields = ('mascota', 'veterinario')


@admin.register(HistorialMedico)
class HistorialMedicoAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'tipo', 'fecha', 'veterinario', 'peso', 'temperatura')
    list_filter = ('tipo', 'fecha', 'veterinario')
    search_fields = ('mascota__nombre', 'diagnostico', 'tratamiento')
    date_hierarchy = 'fecha'
    raw_id_fields = ('mascota', 'veterinario')


@admin.register(Archivo)
class ArchivoAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'tipo', 'titulo', 'fecha', 'fecha_subida')
    list_filter = ('tipo', 'fecha')
    search_fields = ('mascota__nombre', 'titulo', 'descripcion')
    date_hierarchy = 'fecha'
    raw_id_fields = ('mascota', 'historial')