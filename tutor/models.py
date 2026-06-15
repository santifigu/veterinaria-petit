from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

class Tutor(models.Model):
    """Modelo para los tutores/dueños de mascotas"""
    tutor = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100, blank=True, default='')
    apellido = models.CharField(max_length=100, blank=True, default='')
    email = models.EmailField(validators=[EmailValidator()], unique=True, blank=True, default='')
    telefono = models.CharField(max_length=20, blank=True, default='')
    direccion = models.TextField(blank=True, default='')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Tutor"
        verbose_name_plural = "Tutores"
        ordering = ['apellido', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def get_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"