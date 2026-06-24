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
            # ── 1. Guardar en la base de datos (esto SIEMPRE debe funcionar) ──
            contacto_obj = form.save()

            nombre         = form.cleaned_data['nombre']
            apellido       = form.cleaned_data['apellido']
            email          = form.cleaned_data['email']
            telefono       = form.cleaned_data['telefono']
            nombre_mascota = form.cleaned_data['nombre_mascota']
            tipo_consulta  = form.cleaned_data['tipo_consulta']
            mensaje        = form.cleaned_data['mensaje']

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

            # ── 2. Enviar mail (protegido: si falla, NO debe afectar la respuesta) ──
            try:
                send_mail(
                    asunto,
                    cuerpo,
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"⚠️ Error al enviar mail de contacto (id #{contacto_obj.id}): {type(e).__name__}: {e}")

            # ── 3. Responder siempre OK, porque el contacto ya se guardó ──
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})

            messages.success(request, '¡Mensaje enviado con éxito!')
            return redirect('index')

        # Si el form no es válido, vuelve a renderizar con errores
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Revisá los campos del formulario.'})

    return render(request, 'contacto/contacto.html', {'form': form})