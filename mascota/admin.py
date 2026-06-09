from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Mascota, RegistroVacunacion, HistorialMedico, Archivo, ControlAntiparasitario


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
    show_change_link = True


class ArchivoInline(admin.TabularInline):
    model = Archivo
    extra = 0
    fields = ['tipo', 'titulo', 'archivo', 'fecha', 'descripcion']
    verbose_name = "Archivo"
    verbose_name_plural = "📁 Archivos (Rx, análisis, ecografías)"


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('foto_thumbnail', 'nombre', 'tipo', 'raza', 'get_tutor_link', 'peso', 'estado_badge', 'proxima_vacuna', 'activo')
    list_filter = ('tipo', 'sexo', 'estado', 'activo')
    search_fields = ('nombre', 'tutor__nombre', 'tutor__apellido', 'microchip', 'raza')
    raw_id_fields = ('tutor',)
    list_editable = ('activo',)
    readonly_fields = ('fecha_registro', 'foto_preview', 'get_edad')
    date_hierarchy = 'fecha_registro'

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
        return obj.get_edad()
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

    def get_tutor_link(self, obj):
        return format_html(
            '<a href="/admin/tutor/tutor/{}/change/">{}</a>',
            obj.tutor.id, obj.tutor.get_nombre_completo()
        )
    get_tutor_link.short_description = 'Tutor'

    def proxima_vacuna(self, obj):
        vacuna = obj.vacunas.filter(
            proxima_dosis__isnull=False
        ).order_by('proxima_dosis').first()
        if not vacuna:
            return '—'
        hoy = timezone.now().date()
        dias = (vacuna.proxima_dosis - hoy).days
        if dias < 0:
            return format_html('<span style="color:#ef4444;font-weight:700;">⚠️ Vencida</span>')
        elif dias <= 30:
            return format_html('<span style="color:#f59e0b;font-weight:700;">🔔 En {} días</span>', dias)
        return format_html('<span style="color:#22c55e;">✅ {}</span>', vacuna.proxima_dosis)
    proxima_vacuna.short_description = 'Próxima Vacuna'


@admin.register(RegistroVacunacion)
class RegistroVacunacionAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'nombre_vacuna', 'fecha_aplicacion', 'proxima_dosis', 'vencimiento_badge', 'veterinario', 'lote')
    list_filter = ('fecha_aplicacion', 'veterinario', 'nombre_vacuna')
    search_fields = ('mascota__nombre', 'nombre_vacuna', 'lote', 'mascota__tutor__nombre', 'mascota__tutor__apellido')
    date_hierarchy = 'fecha_aplicacion'
    raw_id_fields = ('mascota', 'veterinario')
    autocomplete_fields = []

    def vencimiento_badge(self, obj):
        if not obj.proxima_dosis:
            return '—'
        hoy = timezone.now().date()
        dias = (obj.proxima_dosis - hoy).days
        if dias < 0:
            return format_html('<span style="color:#ef4444;font-weight:700;">⚠️ Vencida hace {} días</span>', abs(dias))
        elif dias <= 30:
            return format_html('<span style="color:#f59e0b;font-weight:700;">🔔 En {} días</span>', dias)
        return format_html('<span style="color:#22c55e;">✅ {}</span>', obj.proxima_dosis)
    vencimiento_badge.short_description = 'Estado Dosis'


@admin.register(ControlAntiparasitario)
class ControlAntiparasitarioAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'antiparasitario', 'fecha', 'peso_en_fecha', 'proxima_desparasitacion', 'proximo_badge', 'veterinario')
    list_filter = ('fecha', 'veterinario')
    search_fields = ('mascota__nombre', 'antiparasitario', 'mascota__tutor__nombre', 'mascota__tutor__apellido')
    date_hierarchy = 'fecha'
    raw_id_fields = ('mascota', 'veterinario')

    def proximo_badge(self, obj):
        if not obj.proxima_desparasitacion:
            return '—'
        hoy = timezone.now().date()
        dias = (obj.proxima_desparasitacion - hoy).days
        if dias < 0:
            return format_html('<span style="color:#ef4444;font-weight:700;">⚠️ Vencido</span>')
        elif dias <= 30:
            return format_html('<span style="color:#f59e0b;font-weight:700;">🔔 En {} días</span>', dias)
        return format_html('<span style="color:#22c55e;">✅ {}</span>', obj.proxima_desparasitacion)
    proximo_badge.short_description = 'Próximo Control'


@admin.register(HistorialMedico)
class HistorialMedicoAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'tipo_badge', 'fecha', 'veterinario', 'peso', 'temperatura', 'proxima_visita')
    list_filter = ('tipo', 'fecha', 'veterinario')
    search_fields = ('mascota__nombre', 'diagnostico', 'tratamiento', 'mascota__tutor__nombre', 'mascota__tutor__apellido')
    date_hierarchy = 'fecha'
    raw_id_fields = ('mascota', 'veterinario')

    def tipo_badge(self, obj):
        colores = {
            'consulta':   ('#3b82f6', '🩺 Consulta'),
            'cirugia':    ('#8b5cf6', '🔪 Cirugía'),
            'emergencia': ('#ef4444', '🚨 Emergencia'),
            'control':    ('#22c55e', '✅ Control'),
            'otro':       ('#6b7280', '📋 Otro'),
        }
        color, label = colores.get(obj.tipo, ('#6b7280', obj.tipo))
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">{}</span>',
            color, label
        )
    tipo_badge.short_description = 'Tipo'


@admin.register(Archivo)
class ArchivoAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'tipo', 'titulo', 'fecha', 'ver_archivo', 'fecha_subida')
    list_filter = ('tipo', 'fecha')
    search_fields = ('mascota__nombre', 'titulo', 'descripcion')
    date_hierarchy = 'fecha'
    raw_id_fields = ('mascota', 'historial')

    def ver_archivo(self, obj):
        if obj.archivo:
            return format_html('<a href="{}" target="_blank">📎 Ver</a>', obj.archivo.url)
        return '—'
    ver_archivo.short_description = 'Archivo'