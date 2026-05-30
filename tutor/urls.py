from django.urls import path
from . import views

app_name = 'tutor'

urlpatterns = [
    path('perfil/', views.perfil_tutor, name='perfil'),
    path('registro/', views.registro_tutor, name='registro'),
    path('actualizar/<int:tutor_id>/', views.actualizar_tutor, name='actualizar'),
]