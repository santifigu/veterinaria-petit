from django.db import models
from django.contrib.auth.models import User # Importamos la tabla de usuarios que se crea con el superuser, es decir, para traer todos los veterinarios registrados en el sistema y asignar un autor a cada post
from ckeditor.fields import RichTextField # Importamos el campo de texto enriquecido para el contenido del post 

# Categorías
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    activo = models.BooleanField(default=True, verbose_name="¿Activo?")
    slug = models.SlugField(max_length=100, unique=True, default="", verbose_name="Slug") # Campo para URL amigable, se genera automáticamente a partir del nombre de la categoría
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación") 
    actualizado_en = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

# Posts
class Post(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    imagen = models.ImageField(upload_to='blog/img/', null=True, blank=True, verbose_name="Imagen")
    bajada = models.CharField(max_length=400, verbose_name="Bajada")
    contenido1 = RichTextField(verbose_name="Contenido 1", null=True, blank=True)
    frase = models.CharField(max_length=400, null=True, blank=True, verbose_name="Frase Destacada")
    contenido2 = RichTextField(verbose_name="Contenido 2", null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, default="", verbose_name="Slug")

    publicado = models.BooleanField(default=True, verbose_name="¿Publicado?")

    categoria = models.ManyToManyField(Categoria, blank=True, verbose_name="Categoría")
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor") # Aca traemos los usuarios que se crean en los super usuarios, para asignar un autor a cada post

    tiempo = models.CharField(max_length=3, default=5, verbose_name="Tiempo de Lectura") # Campo para indicar el tiempo estimado de lectura del post
    publicado_en = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Publicación") 
    actualizado_en = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-publicado_en']

    def __str__(self):
        return self.titulo
