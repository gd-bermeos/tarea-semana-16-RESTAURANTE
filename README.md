# restaurante_app — Semana 16

**Estudiante:** Genessis Daniela Bermeo Sarango  
**Asignatura:** Programación Orientada a Objetos  
**Actividad:** Manejo de eventos en Tkinter aplicado a la gestión de usuarios

## Descripción

Esta versión corresponde a la evolución de `restaurante_app` para la **Semana 16**. Se conservan las funciones principales trabajadas en semanas anteriores: inicio de sesión, gestión de productos, ventas, persistencia mediante archivos JSON y arquitectura modular.

La mejora de esta semana se concentra en la **gestión de usuarios mediante eventos de Tkinter**, incorporando un formulario, una tabla `Treeview`, roles y eventos asociados mediante `bind()`.

## Estructura

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── logo.svg
│   └── usuario.svg
└── main.py

README.md
```

## Gestión de usuarios

La sección **Usuarios** permite registrar, consultar, actualizar y eliminar usuarios. Los registros se muestran en un `ttk.Treeview` con ID, nombre, usuario y rol, sin exponer la contraseña.

Las operaciones de persistencia se realizan mediante `RestauranteServicio`, evitando leer o escribir JSON directamente desde la interfaz.

## Roles implementados

- Administrador
- Empleado
- Cliente

Solo el usuario con rol **Administrador** puede acceder a la gestión administrativa de usuarios.

## Eventos implementados

### 1. `<<TreeviewSelect>>`

Al seleccionar una fila de la tabla, el evento carga automáticamente los datos del usuario en el formulario.

```python
self.tabla_usuarios.bind("<<TreeviewSelect>>", self._seleccionar_usuario)
```

### 2. `<Return>`

La tecla **Enter** registra un usuario reutilizando el método de registro existente.

```python
self.bind_all("<Return>", self._evento_registrar_usuario)
```

### 3. `<Escape>`

La tecla **Escape** limpia el formulario y cancela la selección.

```python
self.bind_all("<Escape>", self._evento_limpiar_usuario)
```

### 4. `<<ComboboxSelected>>`

El `Combobox` de rol responde al cambio de opción mediante un callback.

```python
self.combo_rol.bind("<<ComboboxSelected>>", self._cambio_rol)
```

## Uso de `command=`

Los botones principales conservan `command=`:

- Registrar
- Actualizar
- Eliminar
- Limpiar

Esto permite diferenciar el uso de botones tradicionales frente a eventos asociados mediante `bind()`.

## Flujo de eventos

```text
Interacción del usuario
        ↓
Evento
        ↓
bind()
        ↓
callback(event)
        ↓
RestauranteServicio
        ↓
Persistencia JSON
        ↓
Actualización visual
```

## Persistencia JSON

- `productos.json`: productos y stock.
- `usuarios.json`: usuarios y roles.
- `ventas.json`: ventas realizadas.

`ArchivoServicio` realiza la lectura y escritura de JSON y `RestauranteServicio` concentra las validaciones y reglas de negocio.

## Productos y ventas

La aplicación conserva la gestión de productos y una sección de ventas para mantener la continuidad del proyecto. Al registrar una venta se valida el usuario, el producto, la cantidad y el stock disponible. Después se actualizan `productos.json` y `ventas.json`.

## Recursos visuales

La carpeta `assets/` contiene un logo y un ícono en formato XBM, compatibles con Tkinter para mantener los recursos visuales separados del código.

## Credencial administrativa de prueba

```text
Usuario: admin
Contraseña: admin123
Rol: Administrador
```

## Ejecución

Desde la carpeta `restaurante_app` ejecutar:

```bash
python main.py
```

En Windows también puede utilizarse:

```bash
py main.py
```

## Pruebas principales realizadas

1. Iniciar la aplicación mediante `main.py`.
2. Iniciar sesión como Administrador.
3. Verificar la navegación entre Inicio, Productos, Ventas y Usuarios.
4. Registrar un usuario Empleado o Cliente.
5. Comprobar su aparición en el `Treeview`.
6. Seleccionar una fila y comprobar `<<TreeviewSelect>>`.
7. Actualizar un usuario.
8. Eliminar un usuario con confirmación previa.
9. Verificar que el administrador autenticado no pueda eliminar su propia cuenta.
10. Presionar Enter para registrar mediante `<Return>`.
11. Presionar Escape para limpiar mediante `<Escape>`.
12. Cambiar el rol mediante el `Combobox`.
13. Registrar una venta y comprobar la disminución de stock.
14. Cerrar y volver a ejecutar para comprobar la persistencia en JSON.

## Conclusión

La Semana 16 incorpora el manejo de eventos en Tkinter sin perder la arquitectura modular del proyecto. El uso de `Treeview`, `Combobox`, `bind()`, eventos de teclado y callbacks mejora la interacción de la aplicación, mientras que la lógica de negocio y la persistencia permanecen separadas dentro de los servicios.
