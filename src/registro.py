# src/registro.py
import os
import json
from datetime import datetime
import tkinter.messagebox as messagebox  # 👈 Añade esta línea

# Lista de actividades predefinidas
ACTIVIDADES_PREDEFINIDAS = [
    "Caminata",
    "Running",
    "Trail Running",
    "Ciclismo Ruta",
    "Ciclismo de Montaña",
    "Funcional sin pesas",
    "Funcional con pesas",
    "Movilidad articular dinámica",
    "Elongación",
    "Piscina",
    "Aguas abiertas",
    "Yoga",
    "Pilates"
]

# Grupos de actividades por tipo
GRUPOS_ACTIVIDADES = {
    "correr": [
        "Caminata",
        "Running",
        "Trail Running"
    ],
    "ciclismo": [
        "Ciclismo de Montaña",
        "Ciclismo Ruta"
    ],
    "natacion": [
        "Piscina",
        "Aguas abiertas"
    ],
    "yoga": [
        "Yoga",
        "Pilates"
    ],
    "gimnasio": [
        "Gimnasio",
        "Funcional sin pesas",
        "Funcional con pesas"
    ],
    "movilidad": [
        "Movilidad articular dinámica",
        "Elongación"
    ]
}

# Configuración de campos visibles por grupo
CAMPOS_VISIBILIDAD = {
    "correr": ["fecha", "inicio", "fin", "distancia", "calorias", "lugar"], # "elevacion"
    "ciclismo": ["fecha", "inicio", "fin", "distancia", "calorias", "lugar"], # "ruta_gpx"
    "natacion": ["fecha", "inicio", "fin", "distancia", "lugar"], # "series", "estilo"
    "yoga": ["fecha", "inicio", "fin"], # "duracion_manual", "estilo", "intensidad"
    "gimnasio": ["fecha", "inicio", "fin"], # "duracion_manual", "rutina", "repeticiones"
    "movilidad": ["fecha", "inicio", "fin"]
}

# Ruta dinámica al archivo de datos
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DATOS = os.path.join(directorio_actual, "..", "data", "actividades.json")

def cargar_datos():
    os.makedirs(os.path.dirname(ARCHIVO_DATOS), exist_ok=True)
    
    if not os.path.exists(ARCHIVO_DATOS):
        return []

    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            if not contenido:
                return []
            datos = json.loads(contenido)
    except json.JSONDecodeError as e:
        messagebox.showerror("Error", f"El archivo de datos está corrupto: {e}")
        return []

    # Estructura por defecto para cada actividad
    estructura_por_defecto = {
        "tipo": "Sin tipo",
        "fecha": "Sin fecha",
        "inicio": "",
        "fin": "",
        "duracion_min": "0",
        "distancia_km": "0",
        "calorias_kcal": "0",
        "lugar": "",
        "comentarios": ""
    }

    # Reparar actividades incompletas
    for act in datos:
        for key, value in estructura_por_defecto.items():
            if key not in act:
                act[key] = value

    return datos

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

def calcular_duracion(inicio, fin):
    try:
        h_inicio = datetime.strptime(inicio, "%H:%M")
        h_fin = datetime.strptime(fin, "%H:%M")
        duracion = (h_fin - h_inicio).total_seconds() / 60  # minutos
        return int(duracion)
    except Exception:
        return None

def calcular_estadisticas_por_tipo():
    """Calcula estadísticas detalladas por tipo de actividad"""
    datos = cargar_datos()
    estadisticas = {}

    for act in datos:
        tipo = act.get("tipo", "Otros")
        duracion = act.get("duracion_min", "0")
        distancia = act.get("distancia_km", "0")
        calorias = act.get("calorias_kcal", "0")

        # Inicializar si no existe
        if tipo not in estadisticas:
            estadisticas[tipo] = {
                "cantidad": 0,
                "minutos_totales": 0,
                "km_totales": 0.0,
                "calorias_totales": 0.0
            }

        try:
            estadisticas[tipo]["cantidad"] += 1
            estadisticas[tipo]["minutos_totales"] += int(duracion)
            estadisticas[tipo]["km_totales"] += float(distancia)
            estadisticas[tipo]["calorias_totales"] += float(calorias)
        except (ValueError, TypeError):
            continue  # Ignorar si hay datos inválidos

    # Calcular promedios
    for tipo in estadisticas:
        cant = estadisticas[tipo]["cantidad"]
        estadisticas[tipo]["minutos_promedio"] = round(estadisticas[tipo]["minutos_totales"] / cant, 2) if cant else 0
        estadisticas[tipo]["km_promedio"] = round(estadisticas[tipo]["km_totales"] / cant, 2) if cant else 0.0
        estadisticas[tipo]["calorias_promedio"] = round(estadisticas[tipo]["calorias_totales"] / cant, 2) if cant else 0.0

    return estadisticas