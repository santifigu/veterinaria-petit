from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views
from .views import VRegistro, VPasswordReset, actualizar_perfil, eliminar_cuenta

urlpatterns = [
    path('', VRegistro.as_view(), name="registro"),
    path('perfil/', views.perfil, name='perfil'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('logear/', views.loguear, name='logear'),

    path('password-reset/', VPasswordReset.as_view(
        template_name='registro/password_reset.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registro/password_reset_done.html'
    ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registro/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registro/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('actualizar-perfil/', actualizar_perfil, name='actualizar_perfil'),
    path('eliminar-cuenta/', eliminar_cuenta, name='eliminar_cuenta'),
    path('actualizar-foto-mascota/', views.actualizar_foto_mascota, name='actualizar_foto_mascota'),
    path('eliminar-foto-mascota/', views.eliminar_foto_mascota, name='eliminar_foto_mascota'),
]