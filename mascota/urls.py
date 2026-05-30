from django.urls import path
from . import views

app_name = 'mascota'

urlpatterns = [
    path('agregar/', views.agregar_mascota, name='agregar'),
    path('<int:mascota_id>/editar/', views.editar_mascota, name='editar'),
    path('<int:mascota_id>/eliminar/', views.eliminar_mascota, name='eliminar'),
    path('<int:mascota_id>/cartilla/', views.cartilla_sanitaria, name='cartilla_sanitaria'),
    path('<int:mascota_id>/agregar-vacuna/', views.agregar_vacuna, name='agregar_vacuna'),
]