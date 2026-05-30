from django.contrib import admin
from .models import CategoriaProd, Producto

class CategoriaProdAdmin(admin.ModelAdmin):
    list_display = ("nombre", "created", "updated")
    search_fields = ("nombre",)
    list_filter = ("created", "updated")

class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "categoria", "disponibilidad", "created", "updated")
    search_fields = ("nombre", "descripcion")
    list_filter = ("categoria", "disponibilidad", "created", "updated")

admin.site.register(CategoriaProd, CategoriaProdAdmin)
admin.site.register(Producto, ProductoAdmin)