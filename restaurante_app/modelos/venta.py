class Venta:
    def __init__(self, id, usuario_id, producto_id, cantidad, total):
        self.id = int(id)
        self.usuario_id = int(usuario_id)
        self.producto_id = int(producto_id)
        self.cantidad = int(cantidad)
        self.total = float(total)

    def a_diccionario(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "producto_id": self.producto_id,
            "cantidad": self.cantidad,
            "total": self.total,
        }

    def __str__(self):
        return (
            f"Venta #{self.id} | Usuario: {self.usuario_id} | "
            f"Producto: {self.producto_id} | Cantidad: {self.cantidad} | "
            f"Total: {self.total:.2f}"
        )
