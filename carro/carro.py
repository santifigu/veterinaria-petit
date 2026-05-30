class Carro:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carro = self.session.get("carro")
        if not carro:
            carro = self.session["carro"] = {}
        self.carro = carro

    def agregar(self, producto):
        id_producto = str(producto.id)
        if(id_producto not in self.carro.keys()):
            self.carro[id_producto] = {
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "precio": str(producto.precio),
                "precio_unitario": str(producto.precio),
                "cantidad": 1,
                "imagen": producto.imagen.url
            }
        else:
            for key, value in self.carro.items():
                if key == id_producto:
                    value["cantidad"] = value["cantidad"] + 1
                    # CORRECCIÓN: Convertimos ambos a float antes de sumar
                    value["precio"] = float(value["precio"]) + float(producto.precio)
                    break
        self.guardar_carro()

    def guardar_carro(self):
        self.session["carro"] = self.carro
        self.session.modified = True

    def eliminar(self, producto):
        id_producto = str(producto.id)
        if id_producto in self.carro:
            del self.carro[id_producto]
            self.guardar_carro()

    def restar(self, producto):
        id_producto = str(producto.id)
        for key, value in self.carro.items():
            if key == id_producto:
                value["cantidad"] = value["cantidad"] - 1
                # CORRECCIÓN: Convertimos ambos a float antes de restar
                value["precio"] = float(value["precio"]) - float(producto.precio)
                
                if value["cantidad"] < 1:
                    self.eliminar(producto)
                break
        self.guardar_carro()

    def limpiar_carro(self):
        del self.session["carro"]
        self.session.modified = True