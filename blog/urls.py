from django.urls import include, path
from . import views # Llamamos las vistas desde views

app_name = 'blog' # Para usar namespaces en las URLs

urlpatterns = [
    path('', views.blog, name="blog"),
    # Cambia 'post/' por esto:
    path('post/<int:post_id>/', views.post, name="post"), 
    # Añade una ruta para la redirección al último:
    path('ultimo-post/', views.ultimo_post, name="ultimo_post"),
    path('categoria/<str:categoria_slug>/', views.categoria, name="categoria"),
]