from django.db import models
from django.contrib.auth import get_user_model
from tienda.models import Producto

User = get_user_model()

class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} de {self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    @property
    def total(self):
        total = 0
        for linea in self.lineas.all():
            total += float(linea.producto.precio) * linea.cantidad
        return round(total, 2)

    class Meta:
        db_table = 'Pedidos'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-id']  # corregido: - para más reciente primero


class LineaPedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lineas_usuario')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='lineas')
    cantidad = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cantidad} unidades de {self.producto.nombre} en Pedido #{self.pedido.id}"

    class Meta:
        db_table = 'LineasPedido'
        verbose_name = 'Línea de Pedido'
        verbose_name_plural = 'Líneas de Pedido'
        ordering = ['id']