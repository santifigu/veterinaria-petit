from django.db import models

class Solicitud(models.Model):
    TIPO_MASCOTA = [
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
        ('Otro', 'Otro'),
    ]

    HORARIOS = [
        ('Mañana (9:00 a 12:00)', 'Mañana (9:00 a 12:00)'),
        ('Tarde (14:00 a 16:00)', 'Tarde (14:00 a 16:00)'),
        ('Noche (16:00 a 20:00)', 'Noche (16:00 a 20:00)'),
        ('Sábado (9:00 a 12:00)', 'Sábado (9:00 a 12:00)'),
    ]

    URGENCIA = [
        ('Normal (24 a 48 hs)', 'Normal (24 a 48 hs)'),
        ('Urgente (Mismo día)', 'Urgente (Mismo día)'),
        ('Emergencia (Inmediato)', 'Emergencia (Inmediato)'),
    ]

    nombre = models.CharField(verbose_name="Nombre", max_length=100, null=True)
    apellido = models.CharField(verbose_name="Apellido", max_length=100, null=True)
    nombre_mascota = models.CharField(verbose_name="Nombre de la Mascota", max_length=100)
    tipo_mascota = models.CharField(verbose_name="Tipo de Mascota", max_length=10, choices=TIPO_MASCOTA, null=True)
    email = models.EmailField(verbose_name="Email", max_length=40, unique=True, null=True)
    telefono = models.CharField(verbose_name="Teléfono", max_length=30)
    direccion = models.CharField(verbose_name="Dirección", max_length=200, null=True)
    fecha_preferida = models.DateField(verbose_name="Fecha Preferida", null=True)
    horario_preferido = models.CharField(verbose_name="Horario Preferido", max_length=30, choices=HORARIOS, null=True)
    urgencia = models.CharField(verbose_name="Urgencia", max_length=30, choices=URGENCIA, null=True)
    notas_adicionales = models.TextField(verbose_name="Notas Adicionales", max_length=250, blank=True)

    fecha_envio = models.DateTimeField(verbose_name="Fecha de Envío", auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.tipo_mascota}"
    
    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
        ordering = ['nombre']
