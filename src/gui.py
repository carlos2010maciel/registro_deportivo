# src/gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from src import registro


class RegistroDeportivoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro Deportivo")
        self.root.geometry("400x300")

        self.crear_menu_principal()

    def crear_menu_principal(self):
        """Muestra el menú principal"""
        self.limpiar_ventana()

        tk.Label(self.root, text="Registro Deportivo", font=("Arial", 16)).pack(pady=20)

        ttk.Button(self.root, text="Registrar Nueva Actividad", command=self.mostrar_formulario).pack(pady=10)
        ttk.Button(self.root, text="Ver Registro", command=self.mostrar_registro).pack(pady=10)

    def mostrar_formulario(self):
        """Formulario para registrar una nueva actividad"""
        self.limpiar_ventana()

        tk.Label(self.root, text="Registrar Nueva Actividad", font=("Arial", 14)).pack(pady=10)

        # Campos del formulario
        ttk.Label(self.root, text="Tipo de actividad").pack()
        self.tipo_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.tipo_var).pack()

        ttk.Label(self.root, text="Fecha (YYYY-MM-DD)").pack()
        self.fecha_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.fecha_var).pack()

        ttk.Label(self.root, text="Duración (minutos)").pack()
        self.duracion_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.duracion_var).pack()

        ttk.Label(self.root, text="Distancia (km)").pack()
        self.distancia_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.distancia_var).pack()

        ttk.Label(self.root, text="Comentarios").pack()
        self.comentarios_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.comentarios_var).pack()

        ttk.Button(self.root, text="Guardar", command=self.guardar_actividad).pack(pady=10)
        ttk.Button(self.root, text="Volver", command=self.crear_menu_principal).pack()

    def guardar_actividad(self):
        """Guarda la actividad usando la lógica de registro.py"""
        actividad = {
            "tipo": self.tipo_var.get(),
            "fecha": self.fecha_var.get(),
            "duracion_min": self.duracion_var.get(),
            "distancia_km": self.distancia_var.get(),
            "comentarios": self.comentarios_var.get()
        }

        try:
            datos = registro.cargar_datos()
            datos.append(actividad)
            registro.guardar_datos(datos)
            messagebox.showinfo("Éxito", "Actividad registrada correctamente.")
            self.crear_menu_principal()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la actividad: {e}")

    def mostrar_registro(self):
        """Muestra todas las actividades guardadas"""
        self.limpiar_ventana()

        tk.Label(self.root, text="Registro de Actividades", font=("Arial", 14)).pack(pady=10)

        datos = registro.cargar_datos()

        if not datos:
            tk.Label(self.root, text="No hay actividades registradas.").pack()
        else:
            for idx, act in enumerate(datos):
                texto = f"{idx+1}. {act['tipo']} - {act['fecha']} - {act['duracion_min']} min"
                tk.Label(self.root, text=texto).pack()

        ttk.Button(self.root, text="Volver", command=self.crear_menu_principal).pack(pady=10)

    def limpiar_ventana(self):
        """Limpia todos los widgets de la ventana"""
        for widget in self.root.winfo_children():
            widget.destroy()


def iniciar_gui():
    root = tk.Tk()
    app = RegistroDeportivoApp(root)
    root.mainloop()