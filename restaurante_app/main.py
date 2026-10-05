import tkinter as tk
from pathlib import Path

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


BASE_DIR = Path(__file__).resolve().parent


class RestauranteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurante App - Semana 16")
        self.root.geometry("1120x700")
        self.root.minsize(960, 600)

        self.restaurante_servicio = RestauranteServicio(
            ArchivoServicio(),
            BASE_DIR / "datos" / "usuarios.json",
            BASE_DIR / "datos" / "productos.json",
            BASE_DIR / "datos" / "ventas.json",
        )
        self.vista_actual = None
        self.mostrar_login()

    def _cambiar_vista(self, nueva_vista):
        if self.vista_actual is not None:
            self.vista_actual.destroy()

        self.vista_actual = nueva_vista
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_login(self):
        self._cambiar_vista(
            LoginView(
                self.root,
                self.restaurante_servicio,
                self.mostrar_principal,
            )
        )

    def mostrar_principal(self, usuario):
        self._cambiar_vista(
            MainView(
                self.root,
                self.restaurante_servicio,
                usuario,
                self.mostrar_login,
            )
        )


def main():
    root = tk.Tk()
    RestauranteApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
