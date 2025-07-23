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
        """Limpia todos los campos del formulario accediendo a los Entry en self.campos"""
        for campo in self.campos.values():
            campo["entry"].delete(0, tk.END)  # Borra el contenido del Entry

    def crear_menu_principal(self):
        """Muestra el menú principal"""
        self.limpiar_ventana()

        tk.Label(self.root, text="Registro Deportivo", font=("Arial", 16)).pack(pady=20)

        ttk.Button(self.root, text="Registrar Nueva Actividad", command=self.mostrar_formulario).pack(pady=10)
        ttk.Button(self.root, text="Ver Registro", command=self.mostrar_registro).pack(pady=10)
        ttk.Button(self.root, text="Ver Estadísticas", command=self.mostrar_estadisticas).pack(pady=10)

    def mostrar_formulario(self):
        self.limpiar_ventana()

        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Registrar Nueva Actividad", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        # Campo: Tipo de actividad
        ttk.Label(frame, text="Tipo de actividad").grid(row=1, column=0, sticky="w")
        self.tipo_var = tk.StringVar()
        self.combo_tipo = ttk.Combobox(frame, textvariable=self.tipo_var, values=registro.ACTIVIDADES_PREDEFINIDAS, width=28)
        self.combo_tipo.grid(row=1, column=1, pady=5)
        self.combo_tipo.set("Selecciona o escribe una actividad")
        self.combo_tipo.bind("<<ComboboxSelected>>", lambda e: self.actualizar_visibilidad_campos())

        # Campos posibles (todos se crean, pero se ocultan/muestran dinámicamente)
        self.campos = {}

        # Campo: Fecha
        self.campos["fecha"] = {
            "label": ttk.Label(frame, text="Fecha (YYYY-MM-DD)"),
            "entry": ttk.Entry(frame, textvariable=tk.StringVar(), width=30)
        }
        self.campos["fecha"]["label"].grid(row=2, column=0, sticky="w")
        self.campos["fecha"]["entry"].grid(row=2, column=1, pady=5)

        # Campo: Inicio
        self.campos["inicio"] = {
            "label": ttk.Label(frame, text="Hora de inicio (HH:MM)"),
            "entry": ttk.Entry(frame, textvariable=tk.StringVar(), width=30)
        }
        self.campos["inicio"]["label"].grid(row=3, column=0, sticky="w")
        self.campos["inicio"]["entry"].grid(row=3, column=1, pady=5)

        # Campo: Fin
        self.campos["fin"] = {
            "label": ttk.Label(frame, text="Hora de finalización (HH:MM)"),
            "entry": ttk.Entry(frame, textvariable=tk.StringVar(), width=30)
        }
        self.campos["fin"]["label"].grid(row=4, column=0, sticky="w")
        self.campos["fin"]["entry"].grid(row=4, column=1, pady=5)

        # Campo: Distancia
        self.campos["distancia"] = {
            "label": ttk.Label(frame, text="Distancia (km)"),
            "entry": ttk.Entry(frame, textvariable=tk.StringVar(), width=30)
        }
        self.campos["distancia"]["label"].grid(row=5, column=0, sticky="w")
        self.campos["distancia"]["entry"].grid(row=5, column=1, pady=5)

        # Campo: Calorías
        self.campos["calorias"] = {
            "label": ttk.Label(frame, text="Calorías quemadas (kcal)"),
            "entry": ttk.Entry(frame, textvariable=tk.StringVar(), width=30)
        }
        self.campos["calorias"]["label"].grid(row=6, column=0, sticky="w")
        self.campos["calorias"]["entry"].grid(row=6, column=1, pady=5)

        # Campo: Lugar
        self.campos["lugar"] = {
            "label": ttk.Label(frame, text="Lugar"),
            "entry": ttk.Entry(frame, textvariable=tk.StringVar(), width=30)
        }
        self.campos["lugar"]["label"].grid(row=7, column=0, sticky="w")
        self.campos["lugar"]["entry"].grid(row=7, column=1, pady=5)

        # Campo: Comentarios
        self.campos["comentarios"] = {
            "label": ttk.Label(frame, text="Comentarios"),
            "entry": ttk.Entry(frame, textvariable=tk.StringVar(), width=30)
        }
        self.campos["comentarios"]["label"].grid(row=8, column=0, sticky="w")
        self.campos["comentarios"]["entry"].grid(row=8, column=1, pady=5)

        # Botón Guardar
        ttk.Button(frame, text="Guardar", command=self.guardar_actividad).grid(row=9, column=0, pady=10)
        ttk.Button(frame, text="Cancelar", command=self.crear_menu_principal).grid(row=9, column=1, pady=10)

        # Inicialmente mostrar campos por defecto
        self.actualizar_visibilidad_campos()

    def guardar_actividad(self):
        """Guarda la actividad obteniendo los valores desde self.campos"""
        
        # Obtener valores desde los Entry del formulario
        tipo = self.tipo_var.get().strip()
        fecha = self.campos["fecha"]["entry"].get().strip()
        inicio = self.campos["inicio"]["entry"].get().strip()
        fin = self.campos["fin"]["entry"].get().strip()
        distancia = self.campos["distancia"]["entry"].get().strip()
        calorias = self.campos["calorias"]["entry"].get().strip()
        lugar = self.campos["lugar"]["entry"].get().strip()
        comentarios = self.campos["comentarios"]["entry"].get().strip()

        # Validaciones mínimas
        if not tipo or not fecha:
            messagebox.showwarning("Advertencia", "Tipo y fecha son obligatorios.")
            return

        # Calcular duración si hay hora de inicio y fin
        duracion_calculada = None
        if inicio and fin:
            duracion_calculada = registro.calcular_duracion(inicio, fin)
            if duracion_calculada is None:
                messagebox.showerror("Error", "Horas inválidas. Usa el formato HH:MM.")
                return

        # Crear diccionario con la actividad
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

        if duracion_calculada:
            actividad["duracion_min"] = str(duracion_calculada)

        # Guardar
        try:
            if registro.agregar_actividad(actividad):
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
                texto = f"{idx+1}. {act.get('tipo', 'Sin tipo')} - {act.get('fecha', 'Sin fecha')} - " \
                        f"{act.get('duracion_min', '0')} min - {act.get('distancia_km', '0')} km"
                self.listbox.insert(tk.END, texto)

        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Eliminar seleccionada", command=self.eliminar_seleccionada).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Editar seleccionada", command=self.editar_seleccionada).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Volver", command=self.crear_menu_principal).pack(side="left", padx=5)

    def actualizar_visibilidad_campos(self):
        tipo_seleccionado = self.tipo_var.get()

        # Determinar a qué grupo pertenece
        grupo = None
        for nombre_grupo, tipos in registro.GRUPOS_ACTIVIDADES.items():
            if tipo_seleccionado in tipos:
                grupo = nombre_grupo
                break

        # Determinar qué campos mostrar
        campos_a_mostrar = registro.CAMPOS_VISIBILIDAD.get(grupo, [])

        # Ocultar todos los campos
        for campo in self.campos.values():
            campo["label"].grid_remove()
            campo["entry"].grid_remove()

        # Mostrar solo los relevantes
        fila = 2
        for key in campos_a_mostrar:
            if key in self.campos:
                self.campos[key]["label"].grid(row=fila, column=0, sticky="w")
                self.campos[key]["entry"].grid(row=fila, column=1, pady=5)
                fila += 1

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

    def mostrar_estadisticas(self):
        self.limpiar_ventana()

        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Estadísticas por Tipo de Actividad", font=("Arial", 14)).pack(pady=10)

        # Scrollbar para manejar muchos tipos
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Obtener estadísticas
        stats = registro.calcular_estadisticas_por_tipo()

        if not stats:
            ttk.Label(scrollable_frame, text="No hay actividades registradas.").pack(pady=10)
        else:
            for tipo, datos in stats.items():
                # Frame para cada tipo
                tipo_frame = ttk.LabelFrame(scrollable_frame, text=tipo, padding="5")
                tipo_frame.pack(fill="x", pady=5, padx=10)

                ttk.Label(tipo_frame, text=f"Sesiones: {datos['cantidad']}").grid(row=0, column=0, sticky="w")
                ttk.Label(tipo_frame, text=f"Total minutos: {datos['minutos_totales']}").grid(row=1, column=0, sticky="w")
                ttk.Label(tipo_frame, text=f"Promedio: {datos['minutos_promedio']} min/sesión").grid(row=2, column=0, sticky="w")

                ttk.Label(tipo_frame, text=f"Km totales: {datos['km_totales']} km").grid(row=0, column=1, sticky="w", padx=(20,0))
                ttk.Label(tipo_frame, text=f"Promedio: {datos['km_promedio']} km/sesión").grid(row=1, column=1, sticky="w", padx=(20,0))

                ttk.Label(tipo_frame, text=f"Calorías totales: {datos['calorias_totales']} kcal").grid(row=0, column=2, sticky="w", padx=(20,0))
                ttk.Label(tipo_frame, text=f"Promedio: {datos['calorias_promedio']} kcal/sesión").grid(row=1, column=2, sticky="w", padx=(20,0))

        ttk.Button(frame, text="Volver", command=self.crear_menu_principal).pack(pady=10)

def iniciar_gui():
    root = tk.Tk()
    app = RegistroDeportivoApp(root)
    root.mainloop()