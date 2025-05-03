import customtkinter as ctk
from tkinter import messagebox
import json
import os
from datetime import datetime

class PantallaFuncion(ctk.CTkFrame):
    def __init__(self, master, callback_confirmar, callback_volver, pelicula_seleccionada):
        super().__init__(master)
        self.callback_confirmar = callback_confirmar
        self.callback_volver = callback_volver
        self.pelicula = pelicula_seleccionada
        self.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self, text=f"Película: {self.pelicula}", font=("Arial", 18)).pack(pady=10)
        ctk.CTkLabel(self, text="Selecciona tu función", font=("Arial", 20)).pack(pady=10)

        self.funciones = ["12:00 PM", "3:00 PM", "6:00 PM", "9:00 PM"]
        self.funcion_seleccionada = ctk.StringVar(value=self.funciones[0])

        for funcion in self.funciones:
            ctk.CTkRadioButton(self, text=funcion, variable=self.funcion_seleccionada, value=funcion).pack()

        ctk.CTkLabel(self, text="Selecciona tu asiento", font=("Arial", 16)).pack(pady=10)
        self.asientos = []
        self.seleccion = set()

        grid = ctk.CTkFrame(self)
        grid.pack(pady=10)

        for fila in range(5):
            fila_botones = []
            for col in range(6):
                asiento = ctk.CTkButton(grid, text=f"{fila+1}-{col+1}", width=50,
                                        command=lambda f=fila, c=col: self.seleccionar(f, c))
                asiento.grid(row=fila, column=col, padx=2, pady=2)
                fila_botones.append(asiento)
            self.asientos.append(fila_botones)

        ctk.CTkButton(self, text="Confirmar reserva", command=self.confirmar).pack(pady=10)
        ctk.CTkButton(self, text="Volver", command=lambda: self.callback_volver()).pack(pady=5)

    def seleccionar(self, fila, col):
        clave = f"{fila+1}-{col+1}"
        if clave in self.seleccion:
            self.seleccion.remove(clave)
            self.asientos[fila][col].configure(fg_color=None)
        else:
            self.seleccion.add(clave)
            self.asientos[fila][col].configure(fg_color="green")

    def confirmar(self):
        if not self.seleccion:
            messagebox.showwarning("Sin asiento", "Selecciona al menos un asiento.")
            return

        data = {
            "pelicula": self.pelicula,
            "funcion": self.funcion_seleccionada.get(),
            "asientos": list(self.seleccion)
        }

        registro = {
            "pelicula": data["pelicula"],
            "funcion": data["funcion"],
            "asientos": data["asientos"],
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        ruta_json = "datos/reservas.json"
        os.makedirs("datos", exist_ok=True)

        if os.path.exists(ruta_json):
            with open(ruta_json, "r") as f:
                reservas = json.load(f)
        else:
            reservas = []

        reservas.append(registro)

        with open(ruta_json, "w") as f:
            json.dump(reservas, f, indent=4)

        self.callback_confirmar(data)
