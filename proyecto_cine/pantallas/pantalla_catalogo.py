import customtkinter as ctk
from PIL import Image
import json
import os

class PantallaCatalogo(ctk.CTkFrame):
    def __init__(self, master, callback_ir_a):
        super().__init__(master)
        self.callback_ir_a = callback_ir_a
        self.grid(row=0, column=0, sticky="nsew")
        self.configure(fg_color="#1a1a1a")  # fondo oscuro

        # Título
        ctk.CTkLabel(self, text="Catálogo de Películas", font=("Arial", 22, "bold"), text_color="white").pack(pady=10)

        # Scrollable frame
        scrollable = ctk.CTkScrollableFrame(self, width=800, height=500, fg_color="#2a2a2a")
        scrollable.pack(pady=10, padx=20, fill="both", expand=True)

        ruta_json = os.path.join("datos", "peliculas.json")
        if os.path.exists(ruta_json):
            with open(ruta_json, "r", encoding="utf-8") as archivo:
                peliculas = json.load(archivo)
        else:
            peliculas = []

        for i, peli in enumerate(peliculas):
            imagen_archivo = peli["imagen"]
            ruta_img = os.path.join("imagenes", imagen_archivo)

            if os.path.exists(ruta_img):
                img = Image.open(ruta_img).resize((150, 225))
                img_tk = ctk.CTkImage(img, size=(150, 225))
            else:
                continue  # si no existe la imagen, omitir

            boton = ctk.CTkButton(
                scrollable,
                text=peli["nombre"],
                image=img_tk,
                compound="top",
                width=160,
                height=260,
                font=("Arial", 14),
                command=lambda p=peli["nombre"]: self.callback_ir_a("funcion", p)
            )
            boton.image = img_tk
            boton.grid(row=i // 4, column=i % 4, padx=15, pady=15)

        # Botón de volver dentro del scroll
        ctk.CTkButton(
            scrollable,
            text="Volver al inicio",
            font=("Arial", 16),
            command=lambda: self.callback_ir_a("inicio", None)
        ).grid(column=0, columnspan=4, pady=20)
