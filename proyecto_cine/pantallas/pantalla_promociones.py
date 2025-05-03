import customtkinter as ctk
import json
import os

class PantallaPromociones(ctk.CTkFrame):
    def __init__(self, master, callback_volver):
        super().__init__(master)
        self.callback_volver = callback_volver
        self.grid(row=0, column=0, sticky="nsew")
        self.configure(fg_color="#1f1f1f")  # fondo oscuro cine

        # Título con franja roja
        franja = ctk.CTkFrame(self, fg_color="#cc0000", height=70)
        franja.pack(fill="x")
        titulo = ctk.CTkLabel(franja, text="🎁 Promociones del Cine 🎨", text_color="white", font=("Arial", 24, "bold"))
        titulo.pack(pady=10)

        # Contenido de promociones
        contenido = ctk.CTkFrame(self, fg_color="#1f1f1f")
        contenido.pack(pady=40)

        promociones = self.cargar_promociones()

        for promo in promociones:
            label = ctk.CTkLabel(contenido, text=promo, text_color="white", font=("Arial", 16))
            label.pack(pady=5)

        ctk.CTkButton(self, text="Volver al inicio", command=self.callback_volver).pack(pady=30)

    def cargar_promociones(self):
        ruta = os.path.join("datos", "promociones.json")
        if not os.path.exists(ruta):
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump([], f)
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)



