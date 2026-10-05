import tkinter as tk
from tkinter import messagebox, ttk


class MainView(ttk.Frame):
    def __init__(self, master, restaurante_servicio, usuario_actual, on_logout):
        super().__init__(master, padding=14)
        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.on_logout = on_logout
        self.seccion_actual = "inicio"

        # Productos
        self.prod_id_var = tk.StringVar()
        self.prod_nombre_var = tk.StringVar()
        self.prod_categoria_var = tk.StringVar()
        self.prod_precio_var = tk.StringVar()
        self.prod_cantidad_var = tk.StringVar()
        self.prod_estado_var = tk.StringVar(value="Listo.")
        self.tabla_productos = None

        # Usuarios
        self.user_id_var = tk.StringVar()
        self.user_nombre_var = tk.StringVar()
        self.user_usuario_var = tk.StringVar()
        self.user_contrasena_var = tk.StringVar()
        self.user_rol_var = tk.StringVar(value="Cliente")
        self.user_estado_var = tk.StringVar(value="Seleccione o registre un usuario.")
        self.tabla_usuarios = None
        self.combo_rol = None

        # Ventas
        self.venta_usuario_var = tk.StringVar()
        self.venta_producto_var = tk.StringVar()
        self.venta_cantidad_var = tk.StringVar()
        self.venta_estado_var = tk.StringVar(value="Listo para registrar ventas.")
        self.tabla_ventas = None

        self._construir_interfaz()
        self.bind_all("<Return>", self._evento_registrar_usuario)
        self.bind_all("<Escape>", self._evento_escape)
        self._mostrar_inicio()

    def destroy(self):
        try:
            self.unbind_all("<Return>")
            self.unbind_all("<Escape>")
        except tk.TclError:
            pass
        super().destroy()

    # -------------------- ESTRUCTURA GENERAL --------------------

    def _construir_interfaz(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        encabezado = ttk.Frame(self, padding=(6, 5, 6, 10))
        encabezado.grid(row=0, column=0, columnspan=2, sticky="ew")
        encabezado.columnconfigure(0, weight=1)

        ttk.Label(
            encabezado,
            text="Restaurante App - Semana 16",
            font=("Arial", 19, "bold"),
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(
            encabezado,
            text=f"Sesión: {self.usuario_actual.nombre} ({self.usuario_actual.rol})",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        ttk.Button(
            encabezado,
            text="Cerrar sesión",
            command=self.on_logout,
        ).grid(row=0, column=1, rowspan=2, padx=(20, 0))

        menu = ttk.LabelFrame(self, text="Navegación", padding=10)
        menu.grid(row=1, column=0, sticky="ns", padx=(0, 12))

        ttk.Button(
            menu,
            text="Inicio",
            width=20,
            command=self._mostrar_inicio,
        ).pack(fill="x", pady=4)

        ttk.Button(
            menu,
            text="Productos",
            width=20,
            command=self._mostrar_productos,
        ).pack(fill="x", pady=4)

        ttk.Button(
            menu,
            text="Ventas",
            width=20,
            command=self._mostrar_ventas,
        ).pack(fill="x", pady=4)

        boton_usuarios = ttk.Button(
            menu,
            text="Usuarios",
            width=20,
            command=self._mostrar_usuarios,
        )
        boton_usuarios.pack(fill="x", pady=4)

        if self.usuario_actual.rol != "Administrador":
            boton_usuarios.state(["disabled"])

        self.contenido = ttk.Frame(self, padding=5)
        self.contenido.grid(row=1, column=1, sticky="nsew")
        self.contenido.columnconfigure(0, weight=1)
        self.contenido.rowconfigure(0, weight=1)

    def _limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    # -------------------- INICIO --------------------

    def _mostrar_inicio(self):
        self.seccion_actual = "inicio"
        self._limpiar_contenido()

        panel = ttk.LabelFrame(
            self.contenido,
            text="Resumen del sistema",
            padding=25,
        )
        panel.grid(row=0, column=0, sticky="nsew")
        panel.columnconfigure(0, weight=1)

        ttk.Label(
            panel,
            text="Bienvenido al panel principal",
            font=("Arial", 17, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 15))

        resumen = (
            f"Productos registrados: {self.restaurante_servicio.cantidad_productos()}\n"
            f"Usuarios registrados: {self.restaurante_servicio.cantidad_usuarios()}\n"
            f"Ventas registradas: {self.restaurante_servicio.cantidad_ventas()}\n\n"
            "La Semana 16 incorpora manejo de eventos en la gestión de usuarios.\n"
            "Use el menú lateral para navegar por las opciones disponibles."
        )

        ttk.Label(
            panel,
            text=resumen,
            justify="left",
            font=("Arial", 11),
        ).grid(row=1, column=0, sticky="nw")

    # -------------------- PRODUCTOS --------------------

    def _mostrar_productos(self):
        self.seccion_actual = "productos"
        self._limpiar_contenido()

        contenedor = ttk.Frame(self.contenido)
        contenedor.grid(row=0, column=0, sticky="nsew")
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(2, weight=1)

        ttk.Label(
            contenedor,
            text="Gestión de productos",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        formulario = ttk.LabelFrame(
            contenedor,
            text="Datos del producto",
            padding=12,
        )
        formulario.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        for col in range(5):
            formulario.columnconfigure(col, weight=1)

        campos = [
            ("ID", self.prod_id_var),
            ("Nombre", self.prod_nombre_var),
            ("Categoría", self.prod_categoria_var),
            ("Precio", self.prod_precio_var),
            ("Cantidad", self.prod_cantidad_var),
        ]

        for columna, (texto, variable) in enumerate(campos):
            ttk.Label(formulario, text=f"{texto}:").grid(
                row=0,
                column=columna,
                sticky="w",
                padx=4,
            )
            ttk.Entry(formulario, textvariable=variable).grid(
                row=1,
                column=columna,
                sticky="ew",
                padx=4,
                pady=(3, 8),
            )

        acciones = ttk.Frame(formulario)
        acciones.grid(row=2, column=0, columnspan=5, pady=(4, 0))

        ttk.Button(
            acciones,
            text="Registrar",
            command=self._registrar_producto,
        ).pack(side="left", padx=4)
        ttk.Button(
            acciones,
            text="Cargar",
            command=self._cargar_producto,
        ).pack(side="left", padx=4)
        ttk.Button(
            acciones,
            text="Actualizar",
            command=self._actualizar_producto,
        ).pack(side="left", padx=4)
        ttk.Button(
            acciones,
            text="Eliminar",
            command=self._eliminar_producto,
        ).pack(side="left", padx=4)
        ttk.Button(
            acciones,
            text="Limpiar",
            command=self._limpiar_producto,
        ).pack(side="left", padx=4)

        tabla_frame = ttk.LabelFrame(
            contenedor,
            text="Productos registrados",
            padding=8,
        )
        tabla_frame.grid(row=2, column=0, sticky="nsew")
        tabla_frame.columnconfigure(0, weight=1)
        tabla_frame.rowconfigure(0, weight=1)

        columnas = ("id", "nombre", "categoria", "precio", "cantidad")
        self.tabla_productos = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            height=12,
        )

        encabezados = {
            "id": "ID",
            "nombre": "Producto",
            "categoria": "Categoría",
            "precio": "Precio",
            "cantidad": "Stock",
        }

        for columna in columnas:
            self.tabla_productos.heading(columna, text=encabezados[columna])
            self.tabla_productos.column(columna, anchor="center", width=135)

        barra = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla_productos.yview,
        )
        self.tabla_productos.configure(yscrollcommand=barra.set)
        self.tabla_productos.grid(row=0, column=0, sticky="nsew")
        barra.grid(row=0, column=1, sticky="ns")

        ttk.Label(
            contenedor,
            textvariable=self.prod_estado_var,
        ).grid(row=3, column=0, sticky="w", pady=(8, 0))

        self._actualizar_tabla_productos()

    def _registrar_producto(self):
        try:
            producto = self.restaurante_servicio.registrar_producto(
                self.prod_id_var.get(),
                self.prod_nombre_var.get(),
                self.prod_categoria_var.get(),
                self.prod_precio_var.get(),
                self.prod_cantidad_var.get(),
            )
            self.prod_estado_var.set(
                f"Producto '{producto.nombre}' registrado correctamente."
            )
            self._actualizar_tabla_productos()
            self._limpiar_producto()
        except ValueError as error:
            messagebox.showwarning("Validación", str(error))

    def _cargar_producto(self):
        producto = self.restaurante_servicio.buscar_producto(
            self.prod_id_var.get()
        )

        if producto is None:
            messagebox.showinfo("Consulta", "No se encontró un producto con ese ID.")
            return

        self.prod_id_var.set(str(producto.id))
        self.prod_nombre_var.set(producto.nombre)
        self.prod_categoria_var.set(producto.categoria)
        self.prod_precio_var.set(f"{producto.precio:.2f}")
        self.prod_cantidad_var.set(str(producto.cantidad))
        self.prod_estado_var.set(f"Producto '{producto.nombre}' cargado.")

    def _actualizar_producto(self):
        try:
            producto = self.restaurante_servicio.actualizar_producto(
                self.prod_id_var.get(),
                self.prod_nombre_var.get(),
                self.prod_categoria_var.get(),
                self.prod_precio_var.get(),
                self.prod_cantidad_var.get(),
            )
            self.prod_estado_var.set(
                f"Producto '{producto.nombre}' actualizado correctamente."
            )
            self._actualizar_tabla_productos()
        except ValueError as error:
            messagebox.showwarning("Validación", str(error))

    def _eliminar_producto(self):
        producto = self.restaurante_servicio.buscar_producto(
            self.prod_id_var.get()
        )

        if producto is None:
            messagebox.showinfo("Eliminar", "No se encontró un producto con ese ID.")
            return

        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Desea eliminar el producto '{producto.nombre}'?",
        ):
            return

        try:
            eliminado = self.restaurante_servicio.eliminar_producto(
                self.prod_id_var.get()
            )
            self.prod_estado_var.set(
                f"Producto '{eliminado.nombre}' eliminado correctamente."
            )
            self._actualizar_tabla_productos()
            self._limpiar_producto()
        except ValueError as error:
            messagebox.showwarning("Validación", str(error))

    def _actualizar_tabla_productos(self):
        if self.tabla_productos is None:
            return

        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)

        for producto in self.restaurante_servicio.listar_productos():
            self.tabla_productos.insert(
                "",
                tk.END,
                values=(
                    producto.id,
                    producto.nombre,
                    producto.categoria,
                    f"{producto.precio:.2f}",
                    producto.cantidad,
                ),
            )

    def _limpiar_producto(self):
        self.prod_id_var.set("")
        self.prod_nombre_var.set("")
        self.prod_categoria_var.set("")
        self.prod_precio_var.set("")
        self.prod_cantidad_var.set("")

    # -------------------- USUARIOS Y EVENTOS --------------------

    def _mostrar_usuarios(self):
        if self.usuario_actual.rol != "Administrador":
            messagebox.showwarning(
                "Acceso restringido",
                "Solo el Administrador puede gestionar usuarios.",
            )
            return

        self.seccion_actual = "usuarios"
        self._limpiar_contenido()

        contenedor = ttk.Frame(self.contenido)
        contenedor.grid(row=0, column=0, sticky="nsew")
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(2, weight=1)

        ttk.Label(
            contenedor,
            text="Gestión de usuarios y eventos",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        formulario = ttk.LabelFrame(
            contenedor,
            text="Datos del usuario",
            padding=12,
        )
        formulario.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        for col in range(5):
            formulario.columnconfigure(col, weight=1)

        ttk.Label(formulario, text="ID:").grid(
            row=0, column=0, sticky="w", padx=4
        )
        ttk.Entry(formulario, textvariable=self.user_id_var).grid(
            row=1, column=0, sticky="ew", padx=4, pady=(3, 8)
        )

        ttk.Label(formulario, text="Nombre:").grid(
            row=0, column=1, sticky="w", padx=4
        )
        ttk.Entry(formulario, textvariable=self.user_nombre_var).grid(
            row=1, column=1, sticky="ew", padx=4, pady=(3, 8)
        )

        ttk.Label(formulario, text="Usuario:").grid(
            row=0, column=2, sticky="w", padx=4
        )
        ttk.Entry(formulario, textvariable=self.user_usuario_var).grid(
            row=1, column=2, sticky="ew", padx=4, pady=(3, 8)
        )

        ttk.Label(formulario, text="Contraseña:").grid(
            row=0, column=3, sticky="w", padx=4
        )
        ttk.Entry(
            formulario,
            textvariable=self.user_contrasena_var,
            show="*",
        ).grid(row=1, column=3, sticky="ew", padx=4, pady=(3, 8))

        ttk.Label(formulario, text="Rol:").grid(
            row=0, column=4, sticky="w", padx=4
        )

        self.combo_rol = ttk.Combobox(
            formulario,
            textvariable=self.user_rol_var,
            values=("Administrador", "Empleado", "Cliente"),
            state="readonly",
        )
        self.combo_rol.grid(
            row=1,
            column=4,
            sticky="ew",
            padx=4,
            pady=(3, 8),
        )

        # Evento virtual de Combobox.
        self.combo_rol.bind("<<ComboboxSelected>>", self._cambio_rol)

        acciones = ttk.Frame(formulario)
        acciones.grid(row=2, column=0, columnspan=5, pady=(4, 0))

        # Los botones principales usan command=.
        ttk.Button(
            acciones,
            text="Registrar",
            command=self._registrar_usuario,
        ).pack(side="left", padx=4)
        ttk.Button(
            acciones,
            text="Actualizar",
            command=self._actualizar_usuario,
        ).pack(side="left", padx=4)
        ttk.Button(
            acciones,
            text="Eliminar",
            command=self._eliminar_usuario,
        ).pack(side="left", padx=4)
        ttk.Button(
            acciones,
            text="Limpiar",
            command=self._limpiar_usuario,
        ).pack(side="left", padx=4)

        tabla_frame = ttk.LabelFrame(
            contenedor,
            text="Usuarios registrados",
            padding=8,
        )
        tabla_frame.grid(row=2, column=0, sticky="nsew")
        tabla_frame.columnconfigure(0, weight=1)
        tabla_frame.rowconfigure(0, weight=1)

        columnas = ("id", "nombre", "usuario", "rol")
        self.tabla_usuarios = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            height=12,
            selectmode="browse",
        )

        encabezados = {
            "id": "ID",
            "nombre": "Nombre",
            "usuario": "Usuario",
            "rol": "Rol",
        }

        for columna in columnas:
            self.tabla_usuarios.heading(columna, text=encabezados[columna])
            self.tabla_usuarios.column(columna, anchor="center", width=160)

        barra = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla_usuarios.yview,
        )
        self.tabla_usuarios.configure(yscrollcommand=barra.set)
        self.tabla_usuarios.grid(row=0, column=0, sticky="nsew")
        barra.grid(row=0, column=1, sticky="ns")

        # Evento solicitado: selección del Treeview.
        self.tabla_usuarios.bind(
            "<<TreeviewSelect>>",
            self._seleccionar_usuario,
        )

        ttk.Label(
            contenedor,
            textvariable=self.user_estado_var,
        ).grid(row=3, column=0, sticky="w", pady=(8, 0))

        ttk.Label(
            contenedor,
            text="Atajos: Enter = Registrar | Escape = Limpiar",
            font=("Arial", 9),
        ).grid(row=4, column=0, sticky="w", pady=(4, 0))

        self._actualizar_tabla_usuarios()

    def _registrar_usuario(self):
        try:
            usuario = self.restaurante_servicio.registrar_usuario(
                self.user_id_var.get(),
                self.user_nombre_var.get(),
                self.user_usuario_var.get(),
                self.user_contrasena_var.get(),
                self.user_rol_var.get(),
            )
            self.user_estado_var.set(
                f"Usuario '{usuario.nombre}' registrado correctamente."
            )
            self._actualizar_tabla_usuarios()
            self._limpiar_usuario()
        except ValueError as error:
            messagebox.showwarning("Validación", str(error))

    def _actualizar_usuario(self):
        try:
            usuario = self.restaurante_servicio.actualizar_usuario(
                self.user_id_var.get(),
                self.user_nombre_var.get(),
                self.user_usuario_var.get(),
                self.user_contrasena_var.get(),
                self.user_rol_var.get(),
            )
            self.user_estado_var.set(
                f"Usuario '{usuario.nombre}' actualizado correctamente."
            )
            self._actualizar_tabla_usuarios()
        except ValueError as error:
            messagebox.showwarning("Validación", str(error))

    def _eliminar_usuario(self):
        usuario = self.restaurante_servicio.buscar_usuario(
            self.user_id_var.get()
        )

        if usuario is None:
            messagebox.showinfo("Eliminar", "Seleccione un usuario válido.")
            return

        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Desea eliminar al usuario '{usuario.nombre}'?",
        ):
            return

        try:
            eliminado = self.restaurante_servicio.eliminar_usuario(
                self.user_id_var.get(),
                self.usuario_actual.id,
            )
            self.user_estado_var.set(
                f"Usuario '{eliminado.nombre}' eliminado correctamente."
            )
            self._actualizar_tabla_usuarios()
            self._limpiar_usuario()
        except ValueError as error:
            messagebox.showwarning("Validación", str(error))

    def _seleccionar_usuario(self, event):
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return

        valores = self.tabla_usuarios.item(seleccion[0], "values")
        if not valores:
            return

        # El Treeview conserva solo el ID. La información completa se consulta
        # mediante RestauranteServicio.
        usuario = self.restaurante_servicio.buscar_usuario(valores[0])
        if usuario is None:
            return

        self.user_id_var.set(str(usuario.id))
        self.user_nombre_var.set(usuario.nombre)
        self.user_usuario_var.set(usuario.usuario)
        self.user_contrasena_var.set(usuario.contrasena)
        self.user_rol_var.set(usuario.rol)
        self.user_estado_var.set(
            f"Usuario '{usuario.nombre}' cargado mediante <<TreeviewSelect>>."
        )

    def _cambio_rol(self, event):
        self.user_estado_var.set(
            f"Rol seleccionado: {self.user_rol_var.get()}"
        )

    def _evento_registrar_usuario(self, event):
        if self.seccion_actual == "usuarios":
            # Reutiliza el mismo método del botón Registrar.
            self._registrar_usuario()

    def _evento_escape(self, event):
        if self.seccion_actual == "usuarios":
            self._limpiar_usuario()
        elif self.seccion_actual == "productos":
            self._limpiar_producto()
        elif self.seccion_actual == "ventas":
            self._limpiar_venta()

    def _actualizar_tabla_usuarios(self):
        if self.tabla_usuarios is None:
            return

        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)

        for usuario in self.restaurante_servicio.listar_usuarios():
            self.tabla_usuarios.insert(
                "",
                tk.END,
                values=(
                    usuario.id,
                    usuario.nombre,
                    usuario.usuario,
                    usuario.rol,
                ),
            )

    def _limpiar_usuario(self):
        self.user_id_var.set("")
        self.user_nombre_var.set("")
        self.user_usuario_var.set("")
        self.user_contrasena_var.set("")
        self.user_rol_var.set("Cliente")

        if self.tabla_usuarios is not None:
            for item in self.tabla_usuarios.selection():
                self.tabla_usuarios.selection_remove(item)

        self.user_estado_var.set("Formulario y selección limpiados.")

    # -------------------- VENTAS --------------------

    def _mostrar_ventas(self):
        self.seccion_actual = "ventas"
        self._limpiar_contenido()

        contenedor = ttk.Frame(self.contenido)
        contenedor.grid(row=0, column=0, sticky="nsew")
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(2, weight=1)

        ttk.Label(
            contenedor,
            text="Registro de ventas",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        formulario = ttk.LabelFrame(
            contenedor,
            text="Nueva venta",
            padding=12,
        )
        formulario.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        for col in range(3):
            formulario.columnconfigure(col, weight=1)

        ttk.Label(formulario, text="ID usuario:").grid(
            row=0, column=0, sticky="w", padx=4
        )
        ttk.Entry(formulario, textvariable=self.venta_usuario_var).grid(
            row=1, column=0, sticky="ew", padx=4, pady=(3, 8)
        )

        ttk.Label(formulario, text="ID producto:").grid(
            row=0, column=1, sticky="w", padx=4
        )
        ttk.Entry(formulario, textvariable=self.venta_producto_var).grid(
            row=1, column=1, sticky="ew", padx=4, pady=(3, 8)
        )

        ttk.Label(formulario, text="Cantidad:").grid(
            row=0, column=2, sticky="w", padx=4
        )
        ttk.Entry(formulario, textvariable=self.venta_cantidad_var).grid(
            row=1, column=2, sticky="ew", padx=4, pady=(3, 8)
        )

        acciones = ttk.Frame(formulario)
        acciones.grid(row=2, column=0, columnspan=3)

        ttk.Button(
            acciones,
            text="Registrar venta",
            command=self._registrar_venta,
        ).pack(side="left", padx=4)

        ttk.Button(
            acciones,
            text="Limpiar",
            command=self._limpiar_venta,
        ).pack(side="left", padx=4)

        tabla_frame = ttk.LabelFrame(
            contenedor,
            text="Ventas registradas",
            padding=8,
        )
        tabla_frame.grid(row=2, column=0, sticky="nsew")
        tabla_frame.columnconfigure(0, weight=1)
        tabla_frame.rowconfigure(0, weight=1)

        columnas = ("id", "usuario", "producto", "cantidad", "total")
        self.tabla_ventas = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            height=12,
        )

        encabezados = {
            "id": "Venta",
            "usuario": "ID Usuario",
            "producto": "ID Producto",
            "cantidad": "Cantidad",
            "total": "Total",
        }

        for columna in columnas:
            self.tabla_ventas.heading(columna, text=encabezados[columna])
            self.tabla_ventas.column(columna, anchor="center", width=125)

        self.tabla_ventas.grid(row=0, column=0, sticky="nsew")

        ttk.Label(
            contenedor,
            textvariable=self.venta_estado_var,
        ).grid(row=3, column=0, sticky="w", pady=(8, 0))

        self._actualizar_tabla_ventas()

    def _registrar_venta(self):
        try:
            venta = self.restaurante_servicio.registrar_venta(
                self.venta_usuario_var.get(),
                self.venta_producto_var.get(),
                self.venta_cantidad_var.get(),
            )

            self.venta_estado_var.set(
                f"Venta #{venta.id} registrada. Total: {venta.total:.2f}"
            )
            self._actualizar_tabla_ventas()
            self._limpiar_venta()
        except ValueError as error:
            messagebox.showwarning("Venta", str(error))

    def _actualizar_tabla_ventas(self):
        if self.tabla_ventas is None:
            return

        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)

        for venta in self.restaurante_servicio.listar_ventas():
            self.tabla_ventas.insert(
                "",
                tk.END,
                values=(
                    venta.id,
                    venta.usuario_id,
                    venta.producto_id,
                    venta.cantidad,
                    f"{venta.total:.2f}",
                ),
            )

    def _limpiar_venta(self):
        self.venta_usuario_var.set("")
        self.venta_producto_var.set("")
        self.venta_cantidad_var.set("")
