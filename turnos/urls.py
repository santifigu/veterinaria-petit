from django.urls import path
from . import views

app_name = 'turnos'

urlpatterns = [
    path('', views.turnos, name='turnos'),  
    path('crear/', views.crear_turno, name='crear'),
    path('horarios-disponibles/', views.obtener_horarios_disponibles, name='horarios_disponibles'),
    path('mis-turnos/', views.mis_turnos, name='mis_turnos'),
]