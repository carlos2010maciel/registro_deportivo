# src/registro.py
import json
import os
from datetime import datetime

ARCHIVO_DATOS = "../data/actividades.json"

def cargar_datos():
    if not os.path.exists(ARCHIVO_DATOS):
        return []
    with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_datos(datos):
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
