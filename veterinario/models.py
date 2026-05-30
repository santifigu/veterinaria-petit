from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

class Veterinario(models.Model):
    user = models.OneToOneField(User, verbose_name="Usuario", on_delete=models.CASCADE)
    nombre = models.CharField(verbose_name="Nombre", max_length=100)
    apellido = models.CharField(verbose_name="Apellido", max_length=100)
    matricula = models.CharField(verbose_name="Matrícula", max_length=50, unique=True)
    especialidad = models.CharField(verbose_name="Especialidad", max_length=100, blank=True, null=True)
    telefono = models.CharField(verbose_name="Teléfono", max_length=20)
    email = models.EmailField(verbose_name="Email", max_length=100, validators=[EmailValidator()])
    foto = models.ImageField(verbose_name="Foto de Perfil", upload_to='veterinarios/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Veterinario"
        verbose_name_plural = "Veterinarios"
        ordering = ['apellido', 'nombre']
    
    def __str__(self):
        return f"Dr/a. {self.nombre} {self.apellido} - Mat. {self.matricula}"
    
    def get_nombre_completo(self):
        return f"Dr/a. {self.nombre} {self.apellido}"