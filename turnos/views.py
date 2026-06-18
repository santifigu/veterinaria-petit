from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.utils.formats import date_format
from datetime import datetime, time, timedelta, date
from .models import Turno, Servicio, HorarioDisponible

def turnos(request, template_name='turnos/turnos.html'):
    servicios = Servicio.objects.filter(activo=True)
    context = {
        'servicios': servicios,
        'email_usuario': request.user.email if request.user.is_authenticated else '',
    }
    return render(request, template_name, context)

@require_http_methods(["POST"])
def crear_turno(request):
    try:
        servicio_id    = request.POST.get('servicio_id')
        fecha          = request.POST.get('fecha')
        hora           = request.POST.get('hora')
        nombre_mascota = request.POST.get('nombre_mascota')
        email_cliente  = request.POST.get('email_cliente')

        if not all([servicio_id, fecha, hora, nombre_mascota, email_cliente]):
            return JsonResponse({'success': False, 'error': 'Todos los campos son obligatorios'})

        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        hora_obj  = datetime.strptime(hora, '%H:%M').time()

        if Turno.objects.filter(fecha=fecha_obj, hora=hora_obj, estado__in=['pendiente', 'confirmado']).exists():
            return JsonResponse({'success': False, 'error': 'Este horario ya está reservado'})

        servicio = Servicio.objects.get(id=servicio_id)

        turno = Turno.objects.create(
            servicio=servicio,
            fecha=fecha_obj,
            hora=hora_obj,
            nombre_mascota=nombre_mascota,
            email_cliente=email_cliente,
            estado='confirmado',
            user=request.user if request.user.is_authenticated else None,
        )

        nombre_usuario = request.user.username if request.user.is_authenticated else 'Usuario no registrado'

        # ── Mail al cliente ──
        asunto_cliente = '✅ Turno Confirmado — Córdoba Veterinaria'
        mensaje_cliente = f"""
¡Hola!

Tu turno ha sido confirmado exitosamente. 🐾

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 DETALLES DEL TURNO

🐾 Mascota:  {nombre_mascota}
🩺 Servicio: {servicio.nombre}
📅 Fecha:    {fecha_obj.strftime('%d/%m/%Y')}
⏰ Hora:     {hora_obj.strftime('%H:%M')} hs
💰 Precio:   ${servicio.precio:,.0f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 RETIRO EN SUCURSAL
    Miguel C. Del Corro 56
    Córdoba Capital, Argentina

📞 CONTACTO
    +54 351 444-5566
    veterinaria@cordoba.com

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ IMPORTANTE
    - Llegá 10 minutos antes de tu turno
    - Si necesitás cancelar, avisanos con 24hs de anticipación
    - Traé la cartilla de vacunación de tu mascota

¡Te esperamos!
El equipo de Córdoba Veterinaria 🐶🐱
        """

        # ── Mail a la veterinaria ──
        asunto_vet = f'📅 Nuevo Turno — {nombre_mascota} ({nombre_usuario})'
        mensaje_vet = f"""
Se ha reservado un nuevo turno desde el portal Petit.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 CLIENTE
    Usuario:  {nombre_usuario}
    Email:    {email_cliente}

🐾 MASCOTA
    Nombre:   {nombre_mascota}

🩺 TURNO
    Servicio: {servicio.nombre}
    Fecha:    {fecha_obj.strftime('%d/%m/%Y')}
    Hora:     {hora_obj.strftime('%H:%M')} hs
    Precio:   ${servicio.precio:,.0f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 Ver en el admin:
http://localhost:8000/admin/turnos/turno/{turno.id}/
        """

        try:
            send_mail(asunto_cliente, mensaje_cliente, settings.EMAIL_HOST_USER, [email_cliente], fail_silently=False)
            print(f"✅ Mail al cliente enviado correctamente a {email_cliente}")
        except Exception as e:
            print(f"❌ ERROR al enviar mail al cliente: {type(e).__name__}: {e}")

        try:
            send_mail(asunto_vet, mensaje_vet, settings.EMAIL_HOST_USER, ['santifigu72@gmail.com'], fail_silently=False)
            print(f"✅ Mail a la veterinaria enviado correctamente")
        except Exception as e:
            print(f"❌ ERROR al enviar mail a la veterinaria: {type(e).__name__}: {e}")

        return JsonResponse({'success': True, 'turno_id': turno.id, 'mensaje': '✅ Turno confirmado. Podés ver los detalles en tu perfil.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
@require_http_methods(["GET"])
def obtener_servicios(request):
    """Devuelve los servicios activos en JSON para el modal de modificación."""
    servicios = Servicio.objects.filter(activo=True).values(
        'id', 'nombre', 'precio', 'duracion_minutos', 'imagen_url'
    )
    return JsonResponse({'success': True, 'servicios': list(servicios)})

@require_http_methods(["GET"])
def obtener_horarios_disponibles(request):
    fecha_str = request.GET.get('fecha')
    
    if not fecha_str:
        return JsonResponse({'success': False, 'error': 'Fecha requerida'})
    
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        dia_semana = fecha.weekday()
        es_hoy = fecha == date.today()
        ahora = datetime.now().time()   

        horarios_dia = HorarioDisponible.objects.filter(
            dia_semana=dia_semana,
            activo=True
        )
        
        if not horarios_dia.exists():
            return JsonResponse({'success': True, 'horarios': []})
        
        horarios = []
        
        for horario_config in horarios_dia:
            hora_inicio = datetime.combine(fecha, horario_config.hora_inicio)
            hora_fin    = datetime.combine(fecha, horario_config.hora_fin)
            hora_actual = hora_inicio
            
            while hora_actual <= hora_fin:
                hora_str  = hora_actual.strftime('%H:%M')
                hora_time = hora_actual.time()

                ocupado = Turno.objects.filter(
                    fecha=fecha,
                    hora=hora_time,
                    estado__in=['pendiente', 'confirmado', 'en_curso']
                ).exists()

                # ← Si es hoy y la hora ya pasó, también se bloquea
                ya_paso = es_hoy and hora_time <= ahora

                hora_int = hora_actual.hour
                if 9 <= hora_int < 12:
                    turno = 'mañana'
                elif 12 <= hora_int < 18:
                    turno = 'tarde'
                else:
                    turno = 'noche'

                horarios.append({
                    'hora': hora_str,
                    'disponible': not ocupado and not ya_paso,  # ← combinado
                    'turno': turno
                })
                
                hora_actual += timedelta(minutes=30)
        
        return JsonResponse({'success': True, 'horarios': horarios})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def mis_turnos(request):
    """Vista de turnos del usuario"""
    email = request.GET.get('email')
    
    if not email:
        return render(request, 'turnos/mis_turnos_login.html')
    
    hoy = date.today()
    
    turnos_proximos = Turno.objects.filter(
        email_cliente=email,
        fecha__gte=hoy,
        estado__in=['pendiente', 'confirmado']
    ).select_related('servicio', 'veterinario', 'mascota').order_by('fecha', 'hora')
    
    turnos_pasados = Turno.objects.filter(
        email_cliente=email,
        fecha__lt=hoy
    ).select_related('servicio', 'veterinario', 'mascota').order_by('-fecha', '-hora')[:10]
    
    context = {
        'email': email,
        'turnos_proximos': turnos_proximos,
        'turnos_pasados': turnos_pasados,
        'turnos': turnos_proximos
    }
    
    return render(request, 'turnos/mis_turnos.html', context)

@require_http_methods(["POST"])
def cancelar_turno(request):
    turno_id = request.POST.get('turno_id')
    turno = get_object_or_404(Turno, id=turno_id, user=request.user)
    turno.delete()
    return JsonResponse({'success': True})

def modificar_turno(request):
    if request.method == 'POST':
        turno_id    = request.POST.get('turno_id')
        fecha_str   = request.POST.get('fecha')
        hora_str    = request.POST.get('hora')
        servicio_id = request.POST.get('servicio_id')  # ← nuevo campo

        turno = get_object_or_404(Turno, id=turno_id, user=request.user)

        try:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            hora_obj  = datetime.strptime(hora_str,  '%H:%M').time()

            # Verificar que el nuevo horario no esté ocupado por OTRO turno
            conflicto = Turno.objects.filter(
                fecha=fecha_obj,
                hora=hora_obj,
                estado__in=['pendiente', 'confirmado', 'en_curso']
            ).exclude(id=turno_id).exists()

            if conflicto:
                return JsonResponse({'success': False, 'error': 'Ese horario ya está reservado. Elegí otro.'})

            turno.fecha = fecha_obj
            turno.hora  = hora_obj

            if servicio_id:
                servicio = get_object_or_404(Servicio, id=servicio_id, activo=True)
                turno.servicio = servicio

            turno.save()

            return JsonResponse({
                'success': True,
                'nuevo_dia':              fecha_obj.strftime('%d'),
                'nuevo_mes':              date_format(fecha_obj, 'M'),
                'nueva_fecha_formateada': date_format(fecha_obj, 'l d/m/Y'),
                'nueva_hora':             hora_obj.strftime('%H:%M'),
                'nuevo_servicio_nombre':  turno.servicio.nombre,
                'nuevo_precio':           int(turno.servicio.precio),
            })

        except ValueError:
            return JsonResponse({'success': False, 'error': 'Formato de fecha u hora inválido.'})

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=400)