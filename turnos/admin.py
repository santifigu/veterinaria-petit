from django.contrib import admin
from .models import Servicio, Turno, HorarioDisponible

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'duracion_minutos', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion')
    list_editable = ('activo', 'precio')

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('nombre_mascota', 'servicio', 'fecha', 'hora', 'email_cliente', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha', 'servicio')
    search_fields = ('nombre_mascota', 'email_cliente', 'telefono_cliente')
    date_hierarchy = 'fecha'
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    
    fieldsets = (
        ('Información del Turno', {
            'fields': ('servicio', 'fecha', 'hora', 'estado')
        }),
        ('Información del Cliente', {
            'fields': ('nombre_mascota', 'email_cliente', 'telefono_cliente')
        }),
        ('Notas', {
            'fields': ('notas',),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['marcar_confirmado', 'marcar_completado', 'marcar_cancelado']
    
    def marcar_confirmado(self, request, queryset):
        queryset.update(estado='confirmado')
    marcar_confirmado.short_description = "Marcar como confirmado"
    
    def marcar_completado(self, request, queryset):
        queryset.update(estado='completado')
    marcar_completado.short_description = "Marcar como completado"
    
    def marcar_cancelado(self, request, queryset):
        queryset.update(estado='cancelado')
    marcar_cancelado.short_description = "Marcar como cancelado"

@admin.register(HorarioDisponible)
class HorarioDisponibleAdmin(admin.ModelAdmin):
    list_display = ('get_dia_semana_display', 'hora_inicio', 'hora_fin', 'activo')
    list_filter = ('dia_semana', 'activo')
    list_editable = ('activo',)
