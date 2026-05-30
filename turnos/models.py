from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import User

class Servicio(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=100)
    descripcion = models.TextField(verbose_name="Descripción", blank=True)
    duracion_minutos = models.IntegerField(verbose_name="Duración (minutos)", default=30)
    precio = models.DecimalField(verbose_name="Precio", max_digits=10, decimal_places=2)
    imagen_url = models.URLField(verbose_name="Imagen URL", blank=True, null=True)
    activo = models.BooleanField(verbose_name="Activo", default=True)
    
    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


class Turno(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('en_curso', 'En Curso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.SET_NULL, null=True, blank=True, related_name='turnos')
    mascota = models.ForeignKey('mascota.Mascota', verbose_name="Mascota", on_delete=models.CASCADE, related_name='mascota', null=True, blank=True)
    servicio = models.ForeignKey(Servicio, verbose_name="Servicio", on_delete=models.CASCADE, related_name='turnos')
    veterinario = models.ForeignKey('veterinario.Veterinario', verbose_name="Veterinario", on_delete=models.SET_NULL, null=True, blank=True, related_name='veterinario')
    
    fecha = models.DateField()
    hora = models.TimeField()
    
    # Datos temporales si aún no se registró la mascota
    nombre_mascota = models.CharField(verbose_name="Nombre de la Mascota", max_length=100)
    email_cliente = models.EmailField(verbose_name="Email del Cliente", max_length=100, validators=[EmailValidator()])
    telefono_cliente = models.CharField(verbose_name="Teléfono del Cliente", max_length=20, blank=True, null=True)
    
    estado = models.CharField(verbose_name="Estado", max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    notas = models.TextField(verbose_name="Notas", blank=True, null=True)
    diagnostico = models.TextField(verbose_name="Diagnóstico", blank=True, null=True)
    tratamiento = models.TextField(verbose_name="Tratamiento", blank=True, null=True)
    
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de Creación", auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(verbose_name="Fecha de Actualización", auto_now=True)
    
    class Meta:
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"
        ordering = ['-fecha', '-hora']
        unique_together = ['fecha', 'hora']
    
    def __str__(self):
        return f"{self.nombre_mascota} - {self.servicio.nombre} - {self.fecha} {self.hora}"
    
    def get_precio_formateado(self):
        return f"${self.servicio.precio:,.0f}".replace(",", ".")


class HorarioDisponible(models.Model):
    DIA_SEMANA_CHOICES = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    dia_semana = models.IntegerField(verbose_name="Día de la Semana", choices=DIA_SEMANA_CHOICES)
    hora_inicio = models.TimeField(verbose_name="Hora de Inicio")
    hora_fin = models.TimeField(verbose_name="Hora de Fin")
    activo = models.BooleanField(verbose_name="Activo", default=True)
    
    class Meta:
        verbose_name = "Horario Disponible"
        verbose_name_plural = "Horarios Disponibles"
        ordering = ['dia_semana', 'hora_inicio']
    
    def __str__(self):
        return f"{self.get_dia_semana_display()} - {self.hora_inicio} a {self.hora_fin}"
