import customtkinter as ctk
from PIL import Image
import os

class PantallaInicio(ctk.CTkFrame):
    def __init__(self, master, callback):
        super().__init__(master)
        self.callback = callback
        self.grid(row=0, column=0, sticky="nsew")
        self.configure(fg_color="#1a1a1a")  # Fondo oscuro

        # === Franja roja superior ===
        franja = ctk.CTkFrame(self, fg_color="#b30000", height=100)
        franja.pack(fill="x", side="top")

        # === Logo BUAP (usando CTkImage) ===
        logo_path = os.path.join("imagenes", "buap_logo.jpg")
        self.logo_tk = ctk.CTkImage(Image.open(logo_path), size=(60, 60))  # ✅ CTkImage evita el warning
        logo = ctk.CTkLabel(franja, image=self.logo_tk, text="", fg_color="#b30000")
        logo.pack(side="left", padx=20, pady=10)

        # === Título centrado ===
        ctk.CTkLabel(
            franja,
            text="🎬 Bienvenido al Cine Digital 🎥",
            font=("Arial Rounded MT Bold", 28),
            text_color="white",
            fg_color="#b30000"
        ).pack(pady=25)

        # === Área de botones ===
        cuerpo = ctk.CTkFrame(self, fg_color="#1a1a1a")
        cuerpo.pack(pady=50)

        estilo_boton = {
            "width": 250,
            "height": 50,
            "font": ("Arial", 16),
            "corner_radius": 10,
            "fg_color": "#0056b3",
            "hover_color": "#003f88",
            "text_color": "white"
        }

        ctk.CTkButton(cuerpo, text="🎟 Reservar boletos",
                      command=lambda: self.callback("catalogo", None),
                      **estilo_boton).pack(pady=12)

        ctk.CTkButton(cuerpo, text="🛠 Administrar funciones",
                      command=lambda: self.callback("admin", None),
                      **estilo_boton).pack(pady=12)

        ctk.CTkButton(cuerpo, text="🎁 Ver promociones",
                      command=lambda: self.callback("promociones", None),
                      **estilo_boton).pack(pady=12)
