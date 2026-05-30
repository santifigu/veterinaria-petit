from django.urls import path
from . import views # Llamamos las vistas desde views

urlpatterns = [
    path('', views.tienda, name="tienda"),
    path('checkout/', views.checkout, name="checkout"),
    path('confirmado/', views.confirmado, name="confirmado"),
    path('no_confirmado/', views.no_confirmado, name="no_confirmado"),
    path('pendiente/', views.pendiente, name="pendiente"),
]