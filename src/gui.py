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
    
    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        self.tipo_var.set("")
        self.fecha_var.set("")
        self.duracion_var.set("")
        self.distancia_var.set("")
        self.comentarios_var.set("")

    def crear_menu_principal(self):
        """Muestra el menú principal"""
        self.limpiar_ventana()

        tk.Label(self.root, text="Registro Deportivo", font=("Arial", 16)).pack(pady=20)

        ttk.Button(self.root, text="Registrar Nueva Actividad", command=self.mostrar_formulario).pack(pady=10)
        ttk.Button(self.root, text="Ver Registro", command=self.mostrar_registro).pack(pady=10)

    def mostrar_formulario(self):
        """Formulario organizado para registrar una nueva actividad"""
        self.limpiar_ventana()

        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Registrar Nueva Actividad", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        # Campos del formulario
        # Campo: Tipo de actividad
        ttk.Label(frame, text="Tipo de actividad").grid(row=1, column=0, sticky="w")
        self.tipo_var = tk.StringVar()
        self.combo_tipo = ttk.Combobox(frame, textvariable=self.tipo_var, values=registro.ACTIVIDADES_PREDEFINIDAS, width=28)
        self.combo_tipo.grid(row=1, column=1, pady=5)
        self.combo_tipo.set("Selecciona o escribe una actividad")

        # Campo: Fecha
        ttk.Label(frame, text="Fecha (YYYY-MM-DD)").grid(row=2, column=0, sticky="w")
        self.fecha_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.fecha_var, width=30).grid(row=2, column=1, pady=5)

        # Campo: Hora de inicio
        ttk.Label(frame, text="Hora de inicio (HH:MM)").grid(row=6, column=0, sticky="w")
        self.inicio_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.inicio_var, width=30).grid(row=6, column=1, pady=5)

        # Campo: Hora de finalización
        ttk.Label(frame, text="Hora de finalización (HH:MM)").grid(row=7, column=0, sticky="w")
        self.fin_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.fin_var, width=30).grid(row=7, column=1, pady=5)

        # Campo: Calorías
        ttk.Label(frame, text="Calorías quemadas (kcal)").grid(row=8, column=0, sticky="w")
        self.calorias_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.calorias_var, width=30).grid(row=8, column=1, pady=5)

        # Campo: Lugar
        ttk.Label(frame, text="Lugar").grid(row=9, column=0, sticky="w")
        self.lugar_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.lugar_var, width=30).grid(row=9, column=1, pady=5)

        # Campo: Duración
        ttk.Label(frame, text="Duración (minutos)").grid(row=3, column=0, sticky="w")
        self.duracion_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.duracion_var, width=30).grid(row=3, column=1, pady=5)

        # Campo: Distancia
        ttk.Label(frame, text="Distancia (km)").grid(row=4, column=0, sticky="w")
        self.distancia_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.distancia_var, width=30).grid(row=4, column=1, pady=5)

        # Campo: Comentarios
        ttk.Label(frame, text="Comentarios").grid(row=5, column=0, sticky="w")
        self.comentarios_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.comentarios_var, width=30).grid(row=5, column=1, pady=5)

        # Botones del formulario
        # Botón guardar
        ttk.Button(frame, text="Guardar", command=self.guardar_actividad).grid(row=6, column=0, pady=10)
        # Botón volver
        ttk.Button(frame, text="Volver", command=self.crear_menu_principal).grid(row=6, column=1, pady=10)

    def guardar_actividad(self):
        # Obtener datos del formulario
        tipo = self.tipo_var.get().strip()
        fecha = self.fecha_var.get().strip()
        inicio = self.inicio_var.get().strip()
        fin = self.fin_var.get().strip()
        distancia = self.distancia_var.get().strip()
        calorias = self.calorias_var.get().strip()
        lugar = self.lugar_var.get().strip()
        comentarios = self.comentarios_var.get().strip()

        # Validaciones mínimas
        if not tipo or not fecha:
            messagebox.showwarning("Advertencia", "Tipo y fecha son obligatorios.")
            return

        # Calcular duración si se ingresan ambas horas
        duracion_calculada = None
        if inicio and fin:
            duracion_calculada = registro.calcular_duracion(inicio, fin)
            if duracion_calculada is None:
                messagebox.showerror("Error", "Horas inválidas. Usa el formato HH:MM.")
                return

        # ✅ Aquí defines 'actividad' después de validar y calcular
        actividad = {
            "tipo": tipo,
            "fecha": fecha,
            "inicio": inicio,
            "fin": fin,
            "distancia_km": distancia,
            "calorias_kcal": calorias,
            "lugar": lugar,
            "comentarios": comentarios,
        }

        # Agregar duración calculada si existe
        if duracion_calculada:
            actividad["duracion_min"] = str(duracion_calculada)

        # Guardar actividad
        try:
            datos = registro.cargar_datos()
            datos.append(actividad)
            registro.guardar_datos(datos)
            messagebox.showinfo("Éxito", "Actividad registrada correctamente.")
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

    def mostrar_registro(self):
        """Muestra todas las actividades guardadas con opción de eliminar"""
        self.limpiar_ventana()

        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Registro de Actividades", font=("Arial", 14)).pack(pady=10)

        # Listbox con scrollbar
        listbox_frame = ttk.Frame(frame)
        listbox_frame.pack(pady=10, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, width=60, height=15)
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)

        # Cargar datos
        datos = registro.cargar_datos()
        self.datos_actuales = datos  # Guardamos los datos para usarlos al eliminar

        if not datos:
            self.listbox.insert(tk.END, "No hay actividades registradas.")
        else:
            for idx, act in enumerate(datos):
                texto = f"{idx+1}. {act['tipo']} - {act['fecha']} - {act['duracion_min']} min - {act['distancia_km']} km"
                self.listbox.insert(tk.END, texto)

        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Eliminar seleccionada", command=self.eliminar_seleccionada).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Editar seleccionada", command=self.editar_seleccionada).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Volver", command=self.crear_menu_principal).pack(side="left", padx=5)

    def eliminar_seleccionada(self):
        """Elimina la actividad seleccionada"""
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una actividad.")
            return

        indice = seleccion[0]
        confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta actividad?")
        if confirmacion:
            if registro.eliminar_actividad(indice):
                messagebox.showinfo("Éxito", "Actividad eliminada correctamente.")
                self.mostrar_registro()  # Recargar listado
            else:
                messagebox.showerror("Error", "No se pudo eliminar la actividad.")

    def editar_seleccionada(self):
        """Carga los datos de la actividad seleccionada para editarla"""
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una actividad.")
            return

        self.indice_editar = seleccion[0]  # Guardamos el índice para usarlo luego
        actividad = self.datos_actuales[self.indice_editar]

        self.limpiar_ventana()

        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Editar Actividad", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        # Campo: Tipo de actividad (con Combobox)
        ttk.Label(frame, text="Tipo de actividad").grid(row=1, column=0, sticky="w")
        self.tipo_var = tk.StringVar(value=actividad.get("tipo", ""))
        self.combo_tipo = ttk.Combobox(frame, textvariable=self.tipo_var, values=registro.ACTIVIDADES_PREDEFINIDAS, width=28)
        self.combo_tipo.grid(row=1, column=1, pady=5)
        self.combo_tipo.set(actividad.get("tipo", "Selecciona o escribe una actividad"))

        # Campo: Fecha
        ttk.Label(frame, text="Fecha (YYYY-MM-DD)").grid(row=2, column=0, sticky="w")
        self.fecha_var = tk.StringVar(value=actividad.get("fecha", ""))
        ttk.Entry(frame, textvariable=self.fecha_var, width=30).grid(row=2, column=1, pady=5)

        # Campo: Hora de inicio
        ttk.Label(frame, text="Hora de inicio (HH:MM)").grid(row=3, column=0, sticky="w")
        self.inicio_var = tk.StringVar(value=actividad.get("inicio", ""))
        ttk.Entry(frame, textvariable=self.inicio_var, width=30).grid(row=3, column=1, pady=5)

        # Campo: Hora de finalización
        ttk.Label(frame, text="Hora de finalización (HH:MM)").grid(row=4, column=0, sticky="w")
        self.fin_var = tk.StringVar(value=actividad.get("fin", ""))
        ttk.Entry(frame, textvariable=self.fin_var, width=30).grid(row=4, column=1, pady=5)

        # Campo: Distancia
        ttk.Label(frame, text="Distancia (km)").grid(row=5, column=0, sticky="w")
        self.distancia_var = tk.StringVar(value=actividad.get("distancia_km", ""))
        ttk.Entry(frame, textvariable=self.distancia_var, width=30).grid(row=5, column=1, pady=5)

        # Campo: Calorías
        ttk.Label(frame, text="Calorías quemadas (kcal)").grid(row=6, column=0, sticky="w")
        self.calorias_var = tk.StringVar(value=actividad.get("calorias_kcal", ""))
        ttk.Entry(frame, textvariable=self.calorias_var, width=30).grid(row=6, column=1, pady=5)

        # Campo: Lugar
        ttk.Label(frame, text="Lugar").grid(row=7, column=0, sticky="w")
        self.lugar_var = tk.StringVar(value=actividad.get("lugar", ""))
        ttk.Entry(frame, textvariable=self.lugar_var, width=30).grid(row=7, column=1, pady=5)

        # Campo: Comentarios
        ttk.Label(frame, text="Comentarios").grid(row=8, column=0, sticky="w")
        self.comentarios_var = tk.StringVar(value=actividad.get("comentarios", ""))
        ttk.Entry(frame, textvariable=self.comentarios_var, width=30).grid(row=8, column=1, pady=5)

        # Botones
        ttk.Button(frame, text="Guardar Cambios", command=self.guardar_edicion).grid(row=9, column=0, pady=10)
        ttk.Button(frame, text="Cancelar", command=self.mostrar_registro).grid(row=9, column=1, pady=10)
    
    def guardar_edicion(self):
        """Guarda los cambios realizados en una actividad"""
        tipo = self.tipo_var.get().strip()
        fecha = self.fecha_var.get().strip()
        inicio = self.inicio_var.get().strip()
        fin = self.fin_var.get().strip()
        distancia = self.distancia_var.get().strip()
        calorias = self.calorias_var.get().strip()
        lugar = self.lugar_var.get().strip()
        comentarios = self.comentarios_var.get().strip()

        if not tipo or not fecha:
            messagebox.showwarning("Advertencia", "Tipo y fecha son obligatorios.")
            return

        # Calcular duración si se proporcionan hora de inicio y fin
        duracion_calculada = None
        if inicio and fin:
            duracion_calculada = registro.calcular_duracion(inicio, fin)
            if duracion_calculada is None:
                messagebox.showerror("Error", "Horas inválidas. Usa el formato HH:MM.")
                return

        # Crear diccionario con los nuevos datos
        actividad_editada = {
            "tipo": tipo,
            "fecha": fecha,
            "inicio": inicio,
            "fin": fin,
            "distancia_km": distancia,
            "calorias_kcal": calorias,
            "lugar": lugar,
            "comentarios": comentarios,
        }

        if duracion_calculada:
            actividad_editada["duracion_min"] = str(duracion_calculada)

        if registro.editar_actividad(self.indice_editar, actividad_editada):
            messagebox.showinfo("Éxito", "Actividad actualizada correctamente.")
            self.mostrar_registro()
        else:
            messagebox.showerror("Error", "No se pudo actualizar la actividad.")

    def limpiar_ventana(self):
        """Limpia todos los widgets de la ventana"""
        for widget in self.root.winfo_children():
            widget.destroy()

def iniciar_gui():
    root = tk.Tk()
    app = RegistroDeportivoApp(root)
    root.mainloop()