import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from carro.carro import Carro
from pedidos.models import LineaPedido, Pedido
from django.core.mail import send_mail
from django.conf import settings
# 1. IMPORTANTE: Importamos el validador oficial y la excepción de Django
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


@login_required(login_url='/autenticacion/registro')
def procesar_pedido(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    # Leer datos del JSON que manda el frontend
    try:
        datos = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos inválidos'}, status=400)

    nombre      = datos.get('nombre', request.user.get_full_name() or request.user.username)
    # .strip() elimina espacios invisibles al principio o final del texto
    email       = datos.get('email', request.user.email).strip()
    telefono    = datos.get('telefono', '')
    metodo_pago = datos.get('metodo_pago', 'No especificado')

    # 2. VALIDACIÓN ROBUSTA: Si falla, frena acá. No crea Pedido, ni Líneas, ni envía Mails.
    if not email:
        return JsonResponse({'error': 'El correo electrónico es obligatorio.'}, status=400)
    
    try:
        validate_email(email)  # Validador avanzado de Django (detecta malas estructuras y caracteres prohibidos)
    except ValidationError:
        # Devolvemos un error estructurado al Frontend
        return JsonResponse({'error': 'El formato del email no es válido. Revisalo e intentalo de nuevo.'}, status=400)

    # 3. CREACIÓN DEL PEDIDO (Solo se ejecuta si el email pasó la prueba de arriba)
    pedido = Pedido.objects.create(user=request.user)
    carro  = Carro(request)

    lineas_pedido = []
    for key, value in carro.carro.items():
        lineas_pedido.append(
            LineaPedido(
                producto_id=key,
                user=request.user,
                pedido=pedido,
                cantidad=value['cantidad']
            )
        )
    LineaPedido.objects.bulk_create(lineas_pedido)

    lineas_con_nombres = pedido.lineas.select_related('producto').all()

    fecha_local = timezone.localtime(pedido.created_at)
    fecha_str   = fecha_local.strftime('%d/%m/%Y %H:%M')

    # Etiqueta legible del método de pago
    metodos_labels = {
        'tarjeta':       '💳 Tarjeta de Débito/Crédito (en el local)',
        'transferencia': '🏦 Transferencia Bancaria',
        'qr':            '📱 QR en el Local (Mercado Pago / MODO)',
        'efectivo':      '💵 Efectivo al Retirar',
    }
    metodo_label = metodos_labels.get(metodo_pago, metodo_pago)

    # Enviar correos (ahora son 100% seguros de que el mail destino existe en estructura)
    enviar_mail_veterinario(
        pedido=pedido,
        lineas=lineas_con_nombres,
        nombre=nombre,
        email=email,
        telefono=telefono,
        metodo_label=metodo_label,
        fecha_str=fecha_str,
    )

    enviar_mail_cliente(
        pedido=pedido,
        lineas=lineas_con_nombres,
        nombre=nombre,
        email=email,
        metodo_label=metodo_label,
        fecha_str=fecha_str,
    )

    carro.limpiar_carro()
    return JsonResponse({'ok': True, 'pedido_id': pedido.id})


def enviar_mail_veterinario(**kwargs):
    pedido       = kwargs['pedido']
    lineas       = kwargs['lineas']
    nombre       = kwargs['nombre']
    email        = kwargs['email']
    telefono     = kwargs['telefono']
    metodo_label = kwargs['metodo_label']
    fecha_str    = kwargs['fecha_str']

    productos_lista = "\n".join([
        f"  • {l.cantidad}x {l.producto.nombre}  —  ${l.producto.precio} c/u"
        for l in lineas
    ])

    asunto = f"🛍️ Nuevo pedido #{pedido.id} de {nombre}"
    cuerpo = f"""
Has recibido un nuevo pedido desde Petit Veterinaria.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 CLIENTE
    Nombre:    {nombre}
    Email:     {email}
    Teléfono:  {telefono or 'No indicado'}

💳 MÉTODO DE PAGO
    {metodo_label}

📦 PRODUCTOS
{productos_lista}

💰 TOTAL: ${pedido.total}
📅 Fecha:  {fecha_str}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 Ver en el admin:
http://localhost:8000/admin/pedidos/pedido/{pedido.id}/
    """

    send_mail(
        asunto,
        cuerpo,
        settings.EMAIL_HOST_USER,
        ['santifigu72@gmail.com'],
        fail_silently=True,
    )


def enviar_mail_cliente(**kwargs):
    pedido       = kwargs['pedido']
    lineas       = kwargs['lineas']
    nombre       = kwargs['nombre']
    email        = kwargs['email']
    metodo_label = kwargs['metodo_label']
    fecha_str    = kwargs['fecha_str']

    productos_lista = "\n".join([
        f"  • {l.cantidad}x {l.producto.nombre}  —  ${l.producto.precio} c/u"
        for l in lineas
    ])

    asunto = f"✅ Confirmación de tu pedido #{pedido.id} — Petit Veterinaria"
    cuerpo = f"""
¡Hola {nombre}!

Tu pedido fue recibido exitosamente. 🐾

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 DETALLE DEL PEDIDO #{pedido.id}

{productos_lista}

💰 Total:  ${pedido.total}
📅 Fecha:  {fecha_str}

💳 Método de pago elegido:
{metodo_label}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 RETIRO EN SUCURSAL
    Av. Rafael Núñez 4567, Cerro de las Rosas
    Córdoba, Argentina

    Lunes a Viernes: 09:00 – 20:00
    Sábados:         09:00 – 13:00

Presentá este email o mencioná el número de pedido #{pedido.id} al retirar.

¡Gracias por confiar en Petit Veterinaria! 🐶🐱
El equipo de Petit
    """

    send_mail(
        asunto,
        cuerpo,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=True,
    )