import customtkinter as ctk
from tkinter import filedialog, messagebox
import json
import os
from PIL import Image
from customtkinter import CTkImage

class PantallaAdmin(ctk.CTkFrame):
    def __init__(self, master, callback_volver):
        super().__init__(master)
        self.callback_volver = callback_volver
        self.grid(row=0, column=0, sticky="nsew")
        self.configure(fg_color="#1f1f1f")

        self.peliculas_path = "datos/peliculas.json"
        self.promos_path = "datos/promociones.json"
        self.imagen_pelicula = None

        self.titulo = ctk.CTkLabel(self, text="Agregar nueva película", font=("Arial", 20), text_color="white")
        self.titulo.pack(pady=10)

        # --- Campos para agregar películas ---
        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nombre de la película")
        self.entry_nombre.pack(pady=5)

        self.boton_imagen = ctk.CTkButton(self, text="Seleccionar imagen (.jpg)", command=self.seleccionar_imagen)
        self.boton_imagen.pack(pady=5)

        self.entry_horarios = ctk.CTkEntry(self, placeholder_text="Horarios separados por espacio")
        self.entry_horarios.pack(pady=5)

        ctk.CTkButton(self, text="Guardar película", command=self.guardar_pelicula).pack(pady=5)
        ctk.CTkButton(self, text="Volver al inicio", command=self.callback_volver).pack(pady=5)

        # --- Eliminar película ---
        ctk.CTkLabel(self, text="Eliminar una película", font=("Arial", 18), text_color="white").pack(pady=10)
        self.combo_peliculas = ctk.CTkOptionMenu(self, values=self.obtener_nombres(self.peliculas_path))
        self.combo_peliculas.pack(pady=5)
        ctk.CTkButton(self, text="🗑 Eliminar película", fg_color="red", command=self.eliminar_pelicula).pack(pady=5)

        # === AGREGAR PROMOCIONES ===
        ctk.CTkLabel(self, text="Agregar promoción", font=("Arial", 20), text_color="white").pack(pady=(30, 5))
        self.entry_promo = ctk.CTkEntry(self, placeholder_text="Texto de la promoción")
        self.entry_promo.pack(pady=5)
        ctk.CTkButton(self, text="Guardar promoción", command=self.agregar_promocion).pack(pady=5)

        # === ELIMINAR PROMOCIONES ===
        ctk.CTkLabel(self, text="Eliminar promoción", font=("Arial", 18), text_color="white").pack(pady=10)
        self.combo_promos = ctk.CTkOptionMenu(self, values=self.obtener_nombres(self.promos_path))
        self.combo_promos.pack(pady=5)
        ctk.CTkButton(self, text="🗑 Eliminar promoción", fg_color="red", command=self.eliminar_promocion).pack(pady=5)

    def seleccionar_imagen(self):
        file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg")])
        if file_path:
            nombre = os.path.basename(file_path)
            destino = os.path.join("imagenes", nombre)
            if not os.path.exists(destino):
                os.replace(file_path, destino)
            self.imagen_pelicula = nombre

    def guardar_pelicula(self):
        nombre = self.entry_nombre.get().strip()
        horarios = self.entry_horarios.get().split()
        imagen = self.imagen_pelicula

        if not (nombre and horarios and imagen):
            messagebox.showwarning("Campos incompletos", "Completa todos los campos.")
            return

        nueva = {"nombre": nombre, "imagen": imagen, "funciones": horarios}

        with open(self.peliculas_path, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(nueva)
            f.seek(0)
            json.dump(data, f, indent=4)

        messagebox.showinfo("Listo", f"Pelicula '{nombre}' agregada.")
        self.combo_peliculas.configure(values=self.obtener_nombres(self.peliculas_path))

    def eliminar_pelicula(self):
        eliminar = self.combo_peliculas.get()
        if not eliminar:
            return

        with open(self.peliculas_path, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data = [p for p in data if p["nombre"] != eliminar]
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)

        messagebox.showinfo("Eliminado", f"Pelicula '{eliminar}' eliminada.")
        self.combo_peliculas.configure(values=self.obtener_nombres(self.peliculas_path))

    def agregar_promocion(self):
        texto = self.entry_promo.get().strip()
        if not texto:
            return

        with open(self.promos_path, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(texto)
            f.seek(0)
            json.dump(data, f, indent=4)

        messagebox.showinfo("Éxito", "Promoción agregada.")
        self.combo_promos.configure(values=self.obtener_nombres(self.promos_path))

    def eliminar_promocion(self):
        eliminar = self.combo_promos.get()
        if not eliminar:
            return

        with open(self.promos_path, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data = [p for p in data if p != eliminar]
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)

        messagebox.showinfo("Éxito", "Promoción eliminada.")
        self.combo_promos.configure(values=self.obtener_nombres(self.promos_path))

    def obtener_nombres(self, ruta_json):
        try:
            with open(ruta_json, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    if ruta_json == self.peliculas_path:
                        return [p["nombre"] for p in data]
                    else:
                        return data
        except:
            return []
