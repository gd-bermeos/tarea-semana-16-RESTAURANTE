from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
    def __init__(
        self,
        archivo_servicio,
        ruta_usuarios,
        ruta_productos,
        ruta_ventas,
    ):
        self.archivo_servicio = archivo_servicio
        self.ruta_usuarios = ruta_usuarios
        self.ruta_productos = ruta_productos
        self.ruta_ventas = ruta_ventas
        self.usuarios = []
        self.productos = []
        self.ventas = []
        self.recargar_datos()

    def recargar_datos(self):
        datos_usuarios = self.archivo_servicio.leer_json(self.ruta_usuarios)
        datos_productos = self.archivo_servicio.leer_json(self.ruta_productos)
        datos_ventas = self.archivo_servicio.leer_json(self.ruta_ventas)

        self.usuarios = [Usuario(**dato) for dato in datos_usuarios]
        self.productos = [Producto(**dato) for dato in datos_productos]
        self.ventas = [Venta(**dato) for dato in datos_ventas]

    # -------------------- ACCESO --------------------

    def validar_acceso(self, nombre_usuario, contrasena):
        nombre_usuario = str(nombre_usuario).strip()
        contrasena = str(contrasena).strip()

        if not nombre_usuario or not contrasena:
            return None

        for usuario in self.usuarios:
            if (
                usuario.usuario == nombre_usuario
                and usuario.contrasena == contrasena
            ):
                return usuario
        return None

    # -------------------- USUARIOS --------------------

    def listar_usuarios(self):
        return list(self.usuarios)

    def cantidad_usuarios(self):
        return len(self.usuarios)

    def buscar_usuario(self, id_usuario):
        try:
            id_usuario = int(str(id_usuario).strip())
        except ValueError:
            return None

        for usuario in self.usuarios:
            if usuario.id == id_usuario:
                return usuario
        return None

    def registrar_usuario(self, id_usuario, nombre, usuario, contrasena, rol):
        datos = self._validar_usuario(
            id_usuario, nombre, usuario, contrasena, rol
        )

        if self.buscar_usuario(datos["id"]) is not None:
            raise ValueError("Ya existe un usuario con ese ID.")

        if any(u.usuario.lower() == datos["usuario"].lower() for u in self.usuarios):
            raise ValueError("Ese nombre de usuario ya está registrado.")

        nuevo = Usuario(**datos)
        self.usuarios.append(nuevo)
        self._guardar_usuarios()
        return nuevo

    def actualizar_usuario(self, id_usuario, nombre, usuario, contrasena, rol):
        datos = self._validar_usuario(
            id_usuario, nombre, usuario, contrasena, rol
        )
        existente = self.buscar_usuario(datos["id"])

        if existente is None:
            raise ValueError("No existe un usuario con ese ID.")

        for otro in self.usuarios:
            if (
                otro.id != existente.id
                and otro.usuario.lower() == datos["usuario"].lower()
            ):
                raise ValueError("Ese nombre de usuario ya está registrado.")

        existente.nombre = datos["nombre"]
        existente.usuario = datos["usuario"]
        existente.contrasena = datos["contrasena"]
        existente.rol = datos["rol"]
        self._guardar_usuarios()
        return existente

    def eliminar_usuario(self, id_usuario, id_usuario_actual):
        usuario = self.buscar_usuario(id_usuario)

        if usuario is None:
            raise ValueError("No existe un usuario con ese ID.")

        if usuario.id == int(id_usuario_actual):
            raise ValueError(
                "No puede eliminar la cuenta administrativa actualmente autenticada."
            )

        self.usuarios.remove(usuario)
        self._guardar_usuarios()
        return usuario

    def _validar_usuario(self, id_usuario, nombre, usuario, contrasena, rol):
        nombre = str(nombre).strip()
        usuario = str(usuario).strip()
        contrasena = str(contrasena).strip()
        rol = str(rol).strip()

        if not nombre or not usuario or not contrasena or not rol:
            raise ValueError("Todos los campos del usuario son obligatorios.")

        try:
            id_num = int(str(id_usuario).strip())
        except ValueError as error:
            raise ValueError("El ID del usuario debe ser un número entero.") from error

        if id_num <= 0:
            raise ValueError("El ID debe ser mayor que cero.")

        if rol not in Usuario.ROLES_VALIDOS:
            raise ValueError("Seleccione un rol válido.")

        return {
            "id": id_num,
            "nombre": nombre,
            "usuario": usuario,
            "contrasena": contrasena,
            "rol": rol,
        }

    def _guardar_usuarios(self):
        datos = [usuario.a_diccionario() for usuario in self.usuarios]
        self.archivo_servicio.escribir_json(self.ruta_usuarios, datos)

    # -------------------- PRODUCTOS --------------------

    def listar_productos(self):
        return list(self.productos)

    def cantidad_productos(self):
        return len(self.productos)

    def buscar_producto(self, id_producto):
        try:
            id_producto = int(str(id_producto).strip())
        except ValueError:
            return None

        for producto in self.productos:
            if producto.id == id_producto:
                return producto
        return None

    def registrar_producto(self, id_producto, nombre, categoria, precio, cantidad):
        datos = self._validar_producto(
            id_producto, nombre, categoria, precio, cantidad
        )

        if self.buscar_producto(datos["id"]) is not None:
            raise ValueError("Ya existe un producto con ese ID.")

        producto = Producto(**datos)
        self.productos.append(producto)
        self._guardar_productos()
        return producto

    def actualizar_producto(self, id_producto, nombre, categoria, precio, cantidad):
        datos = self._validar_producto(
            id_producto, nombre, categoria, precio, cantidad
        )
        producto = self.buscar_producto(datos["id"])

        if producto is None:
            raise ValueError("No existe un producto con ese ID.")

        producto.nombre = datos["nombre"]
        producto.categoria = datos["categoria"]
        producto.precio = datos["precio"]
        producto.cantidad = datos["cantidad"]
        self._guardar_productos()
        return producto

    def eliminar_producto(self, id_producto):
        producto = self.buscar_producto(id_producto)

        if producto is None:
            raise ValueError("No existe un producto con ese ID.")

        self.productos.remove(producto)
        self._guardar_productos()
        return producto

    def _validar_producto(self, id_producto, nombre, categoria, precio, cantidad):
        nombre = str(nombre).strip()
        categoria = str(categoria).strip()

        if not nombre or not categoria:
            raise ValueError("Nombre y categoría son obligatorios.")

        try:
            id_num = int(str(id_producto).strip())
        except ValueError as error:
            raise ValueError("El ID debe ser un número entero.") from error

        try:
            precio_num = float(str(precio).strip().replace(",", "."))
        except ValueError as error:
            raise ValueError("El precio debe ser un número válido.") from error

        try:
            cantidad_num = int(str(cantidad).strip())
        except ValueError as error:
            raise ValueError("La cantidad debe ser un número entero.") from error

        if id_num <= 0:
            raise ValueError("El ID debe ser mayor que cero.")
        if precio_num < 0:
            raise ValueError("El precio no puede ser negativo.")
        if cantidad_num < 0:
            raise ValueError("La cantidad no puede ser negativa.")

        return {
            "id": id_num,
            "nombre": nombre,
            "categoria": categoria,
            "precio": precio_num,
            "cantidad": cantidad_num,
        }

    def _guardar_productos(self):
        datos = [producto.a_diccionario() for producto in self.productos]
        self.archivo_servicio.escribir_json(self.ruta_productos, datos)

    # -------------------- VENTAS --------------------

    def listar_ventas(self):
        return list(self.ventas)

    def cantidad_ventas(self):
        return len(self.ventas)

    def registrar_venta(self, usuario_id, producto_id, cantidad):
        usuario = self.buscar_usuario(usuario_id)
        if usuario is None:
            raise ValueError("El usuario indicado no existe.")

        producto = self.buscar_producto(producto_id)
        if producto is None:
            raise ValueError("El producto indicado no existe.")

        try:
            cantidad_num = int(str(cantidad).strip())
        except ValueError as error:
            raise ValueError("La cantidad debe ser un número entero.") from error

        if cantidad_num <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        if producto.cantidad < cantidad_num:
            raise ValueError("No existe stock suficiente para realizar la venta.")

        nuevo_id = max((venta.id for venta in self.ventas), default=0) + 1
        total = producto.precio * cantidad_num

        venta = Venta(
            id=nuevo_id,
            usuario_id=usuario.id,
            producto_id=producto.id,
            cantidad=cantidad_num,
            total=total,
        )

        producto.cantidad -= cantidad_num
        self.ventas.append(venta)

        self._guardar_productos()
        self._guardar_ventas()
        return venta

    def _guardar_ventas(self):
        datos = [venta.a_diccionario() for venta in self.ventas]
        self.archivo_servicio.escribir_json(self.ruta_ventas, datos)
