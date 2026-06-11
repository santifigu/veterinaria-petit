from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from mascota.models import Mascota, ControlAntiparasitario
from .forms import RegistroForm
from pedidos.models import Pedido
from turnos.models import Turno
from django.contrib.auth.views import PasswordResetView # Importar la vista de restablecimiento de contraseña
from django.contrib.auth.models import User # Importar el modelo User para verificar la existencia del usuario durante el restablecimiento de contraseña
from django.http import JsonResponse
from tutor.models import Tutor
import json

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

    # ← Turnos del usuario por email
    turnos_usuario = Turno.objects.filter(
    user=request.user,
    estado__in=['pendiente', 'confirmado', 'en_curso']
    ).select_related('servicio').order_by('fecha', 'hora')

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