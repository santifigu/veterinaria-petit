from django.db import models

class Contacto(models.Model):
    OPCIONES_TIPO = [
        ('Emergencia', 'Emergencia'),
        ('Solicitar Turno', 'Solicitar Turno'),
        ('Consulta General', 'Consulta General'),
        ('Atención a Domicilio', 'Atención a Domicilio'),
        ('Peluquería', 'Peluquería'),
        ('Otro', 'Otro'),
    ]

    nombre = models.CharField(verbose_name="Nombre", max_length=100, null=True)
    apellido = models.CharField(verbose_name="Apellido", max_length=100, null=True)
    email = models.EmailField(verbose_name="Email", null=True)
    telefono = models.CharField(verbose_name="Teléfono", max_length=30)
    nombre_mascota = models.CharField(verbose_name="Nombre Mascota", max_length=100)
    tipo_consulta = models.CharField(verbose_name="Tipo de Consulta", max_length=50, choices=OPCIONES_TIPO, null=True)
    mensaje = models.TextField(verbose_name="Mensaje", max_length=500)
    
    fecha_envio = models.DateTimeField(verbose_name="Fecha de Envío", auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.tipo_consulta}"

