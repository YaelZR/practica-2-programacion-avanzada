import customtkinter as ctk
from pantallas.pantalla_inicio import PantallaInicio
from pantallas.pantalla_catalogo import PantallaCatalogo
from pantallas.pantalla_funcion import PantallaFuncion
from pantallas.pantalla_admin import PantallaAdmin
from pantallas.pantalla_promociones import PantallaPromociones

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Reservas de Cine")
        self.geometry("900x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.mostrar_inicio()

    def mostrar_inicio(self, *args):
        self.limpiar_pantalla()
        self.inicio = PantallaInicio(self, self.cambiar_pantalla)

    def cambiar_pantalla(self, *args):
        destino = args[0]
        extra = args[1] if len(args) > 1 else None

        self.limpiar_pantalla()

        if destino == "catalogo":
            self.catalogo = PantallaCatalogo(self, self.cambiar_pantalla)
        elif destino == "funcion":
            self.funcion = PantallaFuncion(self, self.mostrar_confirmacion, self.mostrar_inicio, extra)
        elif destino == "admin":
            self.admin = PantallaAdmin(self, self.mostrar_inicio)
        elif destino == "promociones":
            self.promos = PantallaPromociones(self, self.mostrar_inicio)
        elif destino == "inicio":
            self.mostrar_inicio()
        else:
            ctk.CTkLabel(self, text="Pantalla aún no disponible", font=("Arial", 20)).pack(pady=30)

    def mostrar_confirmacion(self, datos):
        self.limpiar_pantalla()
        mensaje = (
            f"🎬 Película: {datos['pelicula']}\n"
            f"🕐 Función: {datos['funcion']}\n"
            f"💺 Asientos: {', '.join(datos['asientos'])}"
        )
        ctk.CTkLabel(self, text="¡Reserva confirmada!", font=("Arial", 22, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text=mensaje, font=("Arial", 16)).pack(pady=10)
        ctk.CTkButton(self, text="Volver al inicio", command=self.mostrar_inicio).pack(pady=20)

    def limpiar_pantalla(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()

