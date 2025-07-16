# src/registro.py
import os
import json
from datetime import datetime
import tkinter.messagebox as messagebox  # 👈 Añade esta línea

# Ruta dinámica al archivo de datos
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DATOS = os.path.join(directorio_actual, "..", "data", "actividades.json")

def cargar_datos():
    os.makedirs(os.path.dirname(ARCHIVO_DATOS), exist_ok=True)
    
    if not os.path.exists(ARCHIVO_DATOS):
        return []  # Si no existe, devolvemos lista vacía
    
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            contenido = f.read()
            if not contenido.strip():  # Archivo vacío
                return []
            return json.loads(contenido)
    except json.JSONDecodeError:
        messagebox.showerror("Error", "El archivo de datos está corrupto.")
        return []

def guardar_datos(datos):
    os.makedirs(os.path.dirname(ARCHIVO_DATOS), exist_ok=True)
    
    # 🔍 Línea de depuración (verifica qué ruta está usando)
    print("Guardando en:", ARCHIVO_DATOS)

    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def nueva_actividad():
    print("\nRegistrar nueva actividad:")
    tipo = input("Tipo de actividad (ej: running, ciclismo): ")
    fecha = input("Fecha (YYYY-MM-DD) [dejar vacío para hoy]: ") or str(datetime.now().date())
    duracion = input("Duración (minutos): ")
    distancia = input("Distancia recorrida (km): ")
    comentarios = input("Comentarios (opcional): ")

    actividad = {
        "tipo": tipo,
        "fecha": fecha,
        "duracion_min": duracion,
        "distancia_km": distancia,
        "comentarios": comentarios
    }

    datos = cargar_datos()
    datos.append(actividad)
    guardar_datos(datos)
    print("✅ Actividad registrada!")

def mostrar_registro():
    datos = cargar_datos()
    if not datos:
        print("No hay actividades registradas.")
        return
    print("\nRegistro de actividades:")
    for idx, act in enumerate(datos):
        print(f"{idx+1}. {act['tipo']} - {act['fecha']} - {act['duracion_min']} min")

def menu_principal():
    while True:
        print("\n=== Registro Deportivo ===")
        print("1. Nueva actividad")
        print("2. Ver registro")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            nueva_actividad()
        elif opcion == "2":
            mostrar_registro()
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

def eliminar_actividad(indice):
    """Elimina una actividad por su índice"""
    datos = cargar_datos()
    if 0 <= indice < len(datos):
        datos.pop(indice)
        guardar_datos(datos)
        return True
    return False

def editar_actividad(indice, nueva_actividad):
    """Edita una actividad por su índice"""
    datos = cargar_datos()
    if 0 <= indice < len(datos):
        datos[indice] = nueva_actividad
        guardar_datos(datos)
        return True
    return False