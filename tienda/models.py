from django.db import models

# Create your models here.
class CategoriaProd(models.Model):
    nombre = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "categoriaProd"
        verbose_name_plural = "categoriasProd"
        ordering = ["-created"]

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(verbose_name="Nombre del producto", max_length=100)
    descripcion = models.TextField(verbose_name="Descripción del producto")
    imagen = models.ImageField(verbose_name="Imagen del producto", upload_to="tienda/", null=True, blank=True)
    precio = models.DecimalField(verbose_name="Precio", max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(CategoriaProd, on_delete=models.CASCADE)
    disponibilidad = models.BooleanField(verbose_name="Disponible", default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"
        ordering = ["-created"]

    def __str__(self):
        return self.nombre