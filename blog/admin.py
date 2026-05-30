from django.contrib import admin
from .models import Categoria, Post

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'slug', 'creado_en', 'actualizado_en')
    list_filter = ('activo', 'creado_en')
    search_fields = ('nombre',)
    list_editable = ('activo',)
    readonly_fields = ('creado_en', 'actualizado_en')
    ordering = ('nombre',)
    
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'slug', 'activo')
        }),
        ('Fechas', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'slug', 'get_categoria', 'publicado', 'publicado_en', 'tiempo')
    list_filter = ('publicado', 'publicado_en', 'categoria', 'autor')
    search_fields = ('titulo', 'bajada', 'contenido1', 'contenido2', 'tiempo')
    filter_horizontal = ('categoria',)
    date_hierarchy = 'publicado_en'
    list_editable = ('publicado',)
    readonly_fields = ('publicado_en', 'actualizado_en')
    ordering = ('-publicado_en',)

    fieldsets = (
        ('Información Principal', {
            'fields': ('titulo', 'autor', 'slug', 'categoria')
        }),
        ('Contenido', {
            'fields': ('bajada', 'contenido1', 'frase', 'contenido2', 'imagen', 'tiempo')
        }),
        ('Publicación', {
            'fields': ('publicado', 'publicado_en', 'actualizado_en')
        }),
    )
    
    def get_categoria(self, obj):
        """Muestra las categorías en list_display (ManyToMany no se puede mostrar directamente)"""
        return ", ".join([cat.nombre for cat in obj.categoria.all()])
    get_categoria.short_description = 'Categorías'