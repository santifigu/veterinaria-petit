from datetime import date
from django.db import models
from django.utils import timezone
from veterinario.models import Veterinario

ESTADO_CHOICES = [
    ('saludable', 'Saludable'),
    ('chequeo', 'Chequeo'),
    ('critico', 'Crítico'),
]

class Mascota(models.Model):
    TIPO_CHOICES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
    ]
    
    SEXO_CHOICES = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
    ]

    ESTADO_CHOICES = [
        ('saludable', 'Saludable'),
        ('chequeo', 'Chequeo'),
        ('critico', 'Crítico'),
    ]
    
    tutor = models.ForeignKey('tutor.Tutor', on_delete=models.CASCADE, related_name='mascotas')
    nombre = models.CharField("Nombre de la Mascota", max_length=100)
    altura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Altura en cm")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='saludable')
    tipo = models.CharField("Tipo", max_length=10, choices=TIPO_CHOICES)
    raza = models.CharField("Raza", max_length=100)
    sexo = models.CharField("Sexo", max_length=10, choices=SEXO_CHOICES)
    fecha_nacimiento = models.DateField("Fecha de Nacimiento", null=True, blank=True)
    color = models.CharField("Color", max_length=100, help_text="Color o particularidad para identificar")
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Peso en kg")
    microchip = models.CharField("Microchip", max_length=50, blank=True, null=True)
    foto = models.ImageField("Foto", upload_to='mascotas/', blank=True, null=True)
    observaciones = models.TextField("Observaciones", blank=True, null=True)
    fecha_registro = models.DateTimeField("Fecha de Registro", auto_now_add=True)
    activo = models.BooleanField("Activo", default=True)

    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()}) - {self.tutor.get_nombre_completo()}"
    
    def get_edad(self):
        if not self.fecha_nacimiento:
            return "Edad desconocida"
        hoy = date.today()
        años = hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
        meses = (hoy.month - self.fecha_nacimiento.month) % 12
        if meses == 0 and (hoy.month, hoy.day) >= (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            meses = 0
        partes = []
        if años > 0:
            partes.append(f"{años} año{'s' if años > 1 else ''}")
        if meses > 0:
            partes.append(f"{meses} mes{'es' if meses > 1 else ''}")
        return " y ".join(partes) if partes else "Recién nacido"

class ControlAntiparasitario(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='antiparasitarios')
    veterinario = models.ForeignKey('veterinario.Veterinario', on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField()
    antiparasitario = models.CharField(max_length=200, help_text="Nombre del producto")
    peso_en_fecha = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Peso en kg al momento del control")
    proxima_desparasitacion = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Control Antiparasitario"
        verbose_name_plural = "Controles Antiparasitarios"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.mascota.nombre} - {self.antiparasitario} - {self.fecha}"


class RegistroVacunacion(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='vacunas')
    veterinario = models.ForeignKey(Veterinario, on_delete=models.SET_NULL, null=True, blank=True)
    
    nombre_vacuna = models.CharField(max_length=100)
    fecha_aplicacion = models.DateField()
    proxima_dosis = models.DateField(null=True, blank=True)
    lote = models.CharField(max_length=50, blank=True, null=True)
    laboratorio = models.CharField(max_length=100, blank=True, null=True)
    
    observaciones = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Registro de Vacunación"
        verbose_name_plural = "Registros de Vacunación"
        ordering = ['-fecha_aplicacion']
    
    def __str__(self):
        return f"{self.mascota.nombre} - {self.nombre_vacuna} - {self.fecha_aplicacion}"


class HistorialMedico(models.Model):
    TIPO_CHOICES = [
        ('consulta', 'Consulta'),
        ('cirugia', 'Cirugía'),
        ('emergencia', 'Emergencia'),
        ('control', 'Control'),
        ('otro', 'Otro'),
    ]
    
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='historial')
    veterinario = models.ForeignKey(Veterinario, on_delete=models.SET_NULL, null=True, blank=True)
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha = models.DateField()
    motivo_consulta = models.TextField()
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    medicamentos = models.TextField(blank=True, null=True)
    examenes = models.TextField(blank=True, null=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    
    observaciones = models.TextField(blank=True, null=True)
    proxima_visita = models.DateField(null=True, blank=True)
    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Historial Médico"
        verbose_name_plural = "Historiales Médicos"
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.mascota.nombre} - {self.tipo} - {self.fecha}"


class Archivo(models.Model):
    TIPO_CHOICES = [
        ('radiografia', 'Radiografía'),
        ('analisis', 'Análisis'),
        ('ecografia', 'Ecografía'),
        ('otro', 'Otro'),
    ]
    
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='archivos')
    historial = models.ForeignKey(HistorialMedico, on_delete=models.CASCADE, null=True, blank=True, related_name='archivos')
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='archivos_mascotas/')
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField()
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Archivo"
        verbose_name_plural = "Archivos"
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.mascota.nombre} - {self.titulo}"