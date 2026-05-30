from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from .models import Contacto
from .forms import ContactoForm

def contacto(request):
    form = ContactoForm()  # Siempre inicializamos el form

    if request.method == 'POST':
        form = ContactoForm(request.POST)

        if form.is_valid():
            try:
                # Guardar en la base de datos
                contacto_obj = form.save()

                # Extraer datos para el email
                nombre = form.cleaned_data['nombre']
                apellido = form.cleaned_data['apellido']
                email = form.cleaned_data['email']
                telefono = form.cleaned_data['telefono']
                nombre_mascota = form.cleaned_data['nombre_mascota']
                tipo_consulta = form.cleaned_data['tipo_consulta']
                mensaje = form.cleaned_data['mensaje']

                asunto = f'Nuevo contacto de {nombre} {apellido} - Córdoba Veterinaria'

                cuerpo = f"""
            Has recibido un nuevo mensaje desde el formulario de contacto:

            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

            👤 DATOS DEL CLIENTE:
                Nombre y Apellido: {nombre} {apellido}
                Teléfono: {telefono}
                Email: {email}

            🐾 DETALLES DEL CONTACTO:
                Nombre de la mascota: {nombre_mascota}
                Tipo de consulta: {tipo_consulta}
            💬 MENSAJE:
            {mensaje}

            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

            Fecha: {contacto_obj.fecha_envio.strftime('%d/%m/%Y %H:%M')}
                            """

                send_mail(
                    asunto,
                    cuerpo,
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )

                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})

                messages.success(request, '¡Mensaje enviado con éxito!')
                return redirect('index')

            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': str(e)})

                messages.error(request, 'Hubo un error al enviar el mensaje. Intenta nuevamente.')

        # Si el form no es válido, vuelve a renderizar con errores
        # (No redirige, para que el usuario vea qué campo está mal)

    return render(request, 'contacto/contacto.html', {'form': form})