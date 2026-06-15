# En tu models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Tutor(models.Model):
    """Modelo para los tutores/dueños de mascotas"""
    tutor = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='perfil_tutor')
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
        if self.nombre or self.apellido:
            return f"{self.nombre} {self.apellido}".strip()
        return self.tutor.username if self.tutor else f"Tutor #{self.id}"
    
    def get_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"


# --- ESTO ES LO NUEVO: SEÑALES (SIGNALS) ---
# Sincronizar Tutor con Usuario

@receiver(post_save, sender=Tutor)
def sincronizar_tutor_con_usuario(sender, instance, created, **kwargs):
    """
    Cada vez que se guarde o modifique un Tutor, copia el nombre, 
    apellido y email hacia el Usuario de Django correspondiente.
    """
    if instance.tutor:
        usuario = instance.tutor
        # Evitamos bucles infinitos verificando si el dato realmente cambió antes de guardar
        cambio = False
        
        if usuario.first_name != instance.nombre:
            usuario.first_name = instance.nombre
            cambio = True
            
        if usuario.last_name != instance.apellido:
            usuario.last_name = instance.apellido
            cambio = True
            
        if usuario.email != instance.email:
            usuario.email = instance.email
            cambio = True
            
        if cambio:
            usuario.save()

# Sincronizar Usuario con Tutor
@receiver(post_save, sender=User)
def sincronizar_usuario_con_tutor(sender, instance, created, **kwargs):
    """
    Si editas el usuario directamente en el panel de Django,
    actualiza los datos en el modelo Tutor.
    """
    # Verificamos si este usuario tiene un Tutor asociado usando el related_name
    if hasattr(instance, 'perfil_tutor') and instance.perfil_tutor:
        tutor = instance.perfil_tutor
        cambio = False
        
        if tutor.nombre != instance.first_name:
            tutor.nombre = instance.first_name
            cambio = True
            
        if tutor.apellido != instance.last_name:
            tutor.apellido = instance.last_name
            cambio = True
            
        if tutor.email != instance.email:
            tutor.email = instance.email
            cambio = True
            
        if cambio:
            tutor.save()