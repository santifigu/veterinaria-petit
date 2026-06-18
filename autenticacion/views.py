from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from urllib3 import request
from mascota.models import Mascota, ControlAntiparasitario
from .forms import RegistroForm
from pedidos.models import Pedido
from turnos.models import Turno
from django.contrib.auth.views import PasswordResetView # Importar la vista de restablecimiento de contraseña
from django.contrib.auth.models import User # Importar el modelo User para verificar la existencia del usuario durante el restablecimiento de contraseña
from django.http import JsonResponse
from tutor.models import Tutor
import json
from datetime import date, timedelta
from django.core.mail import send_mail
from django.conf import settings

@login_required
def perfil(request):
    try:
        mascotas = Mascota.objects.filter(
            tutor__tutor=request.user
        ).prefetch_related(
            'vacunas',
            'antiparasitarios',
            'historial',
            'archivos',
        )
    except Exception:
        mascotas = Mascota.objects.none()

    pedidos = Pedido.objects.filter(
        user=request.user
    ).prefetch_related('lineas__producto').order_by('-created_at')

    hace_30_dias = date.today() - timedelta(days=30)

    turnos_usuario = Turno.objects.filter(
        user=request.user,
        fecha__gte=hace_30_dias,
        estado__in=['pendiente', 'confirmado', 'en_curso']
    ).select_related('servicio').order_by('-fecha', '-hora')

    try:
        tutor = Tutor.objects.get(tutor=request.user)
    except Tutor.DoesNotExist:
        tutor = None

    context = {
        'mascotas': mascotas,
        'pedidos': pedidos,
        'turnos_usuario': turnos_usuario,
        'tutor': tutor,
    }
    return render(request, 'registro/perfil.html', context)


# Vista para el registro de usuarios
class VRegistro(View):
    def get(self, request):
        form = RegistroForm()
        return render(request, 'registro/registro.html', {'form': form})

    def post(self, request):
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario, backend='django.contrib.auth.backends.ModelBackend')
            # ── Mail de bienvenida ──
            if usuario.email:
                asunto = '🐾 ¡Bienvenido a Petit, Córdoba Veterinaria!'
                mensaje = f"""
¡Hola {usuario.username}!

Gracias por registrarte en Petit. Tu cuenta ya está lista para usar. 🐶🐱

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Con tu cuenta podés:

    📅 Reservar turnos para tus mascotas
    🛍️  Comprar productos en nuestra tienda
    📋 Llevar el registro de vacunas y controles
    🐾 Gestionar el perfil de cada una de tus mascotas
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 NUESTRA SUCURSAL
    Miguel C. Del Corro 56
    Córdoba Capital, Argentina

📞 CONTACTO
    +54 351 444-5566
    veterinaria@cordoba.com

¡Te esperamos pronto!
El equipo de Petit 🐾
                """
                try:
                    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [usuario.email], fail_silently=True)
                except Exception as e:
                    print(f"⚠️ Error al enviar mail de bienvenida: {e}")

            messages.success(request, "¡Bienvenido a la familia Petit! Registro exitoso.")
            return redirect('index')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            for error in form.non_field_errors():
                messages.error(request, error)
            return render(request, 'registro/registro.html', {'form': form})



# Vista personalizada para el restablecimiento de contraseña
class VPasswordReset(PasswordResetView):
    template_name = 'registro/password_reset.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            messages.error(self.request, "No existe ninguna cuenta asociada a ese email.")
            return redirect('password_reset')
        return super().form_valid(form)

# Vista para cerrar sesión
def cerrar_sesion(request):
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect('registro')

# Vista para iniciar sesión
def loguear(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get('username')
            contra = form.cleaned_data.get('password')
            usuario = authenticate(request, username=nombre_usuario, password=contra)

            if usuario is not None:
                login(request, usuario, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('index')
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return redirect('registro')

@login_required
def actualizar_perfil(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Datos inválidos'})

    user = request.user
    campo = data.get('campo')
    valor = data.get('valor', '').strip()

    if not valor:
        return JsonResponse({'success': False, 'error': 'El valor no puede estar vacío'})

    try:
        if campo == 'username':
            if User.objects.filter(username=valor).exclude(pk=user.pk).exists():
                return JsonResponse({'success': False, 'error': 'Ese nombre de usuario ya existe'})
            user.username = valor
            user.save()

        elif campo == 'email':
            if User.objects.filter(email=valor).exclude(pk=user.pk).exists():
                return JsonResponse({'success': False, 'error': 'Ese email ya está en uso'})
            user.email = valor
            user.save()
            try:
                tutor = Tutor.objects.get(tutor=user)
                tutor.email = valor
                tutor.save()
            except Tutor.DoesNotExist:
                pass

        elif campo in ['telefono', 'direccion', 'nombre', 'apellido']:
            tutor, created = Tutor.objects.get_or_create(
                tutor=user,
                defaults={
                    'nombre': user.username,
                    'apellido': '',
                    'email': user.email,
                    'telefono': '',
                    'direccion': '',
                }
            )
            setattr(tutor, campo, valor)
            tutor.save()

        else:
            return JsonResponse({'success': False, 'error': 'Campo no válido'})

        return JsonResponse({'success': True, 'valor': valor})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
@login_required
def actualizar_foto_mascota(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

    mascota_id = request.POST.get('mascota_id')
    foto = request.FILES.get('foto')

    if not mascota_id or not foto:
        return JsonResponse({'success': False, 'error': 'Datos incompletos'})

    try:
        from mascota.models import Mascota
        mascota = Mascota.objects.get(id=mascota_id, tutor__tutor=request.user)
        mascota.foto = foto
        mascota.save()
        return JsonResponse({'success': True, 'url': mascota.foto.url})
    except Mascota.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Mascota no encontrada'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
@login_required
def eliminar_foto_mascota(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

    mascota_id = request.POST.get('mascota_id')
    if not mascota_id:
        return JsonResponse({'success': False, 'error': 'Datos incompletos'})

    try:
        mascota = Mascota.objects.get(id=mascota_id, tutor__tutor=request.user)
        if mascota.foto:
            mascota.foto.delete(save=False)
            mascota.foto = None
            mascota.save()
        return JsonResponse({'success': True})
    except Mascota.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Mascota no encontrada'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def eliminar_cuenta(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

    user = request.user
    try:
        try:
            tutor = Tutor.objects.get(tutor=user)
            tutor.delete()
        except Tutor.DoesNotExist:
            pass
        logout(request)
        user.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
