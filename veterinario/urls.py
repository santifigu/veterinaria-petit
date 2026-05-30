from django.urls import path
from . import views

app_name = 'veterinario'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('paciente/<int:mascota_id>/', views.detalle_paciente, name='detalle_paciente'),
    path('paciente/<int:mascota_id>/agregar-historial/', views.agregar_historial, name='agregar_historial'),
]