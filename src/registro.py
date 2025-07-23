# src/registro.py
import os
from src import database
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
    """Carga todas las actividades desde SQLite"""
    try:
        conn = database.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM actividades ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()

        # Convertir filas a lista de diccionarios
        columnas = ["id", "tipo", "fecha", "inicio", "fin", "duracion_min", "distancia_km", "calorias_kcal", "lugar", "comentarios"]
        return [dict(zip(columnas, row)) for row in rows]
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")
        return []

def agregar_actividad(actividad):
    """Guarda una nueva actividad en SQLite"""
    try:
        conn = database.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO actividades 
            (tipo, fecha, inicio, fin, duracion_min, distancia_km, calorias_kcal, lugar, comentarios)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            actividad.get("tipo", ""),
            actividad.get("fecha", ""),
            actividad.get("inicio", ""),
            actividad.get("fin", ""),
            actividad.get("duracion_min", "0"),
            actividad.get("distancia_km", "0"),
            actividad.get("calorias_kcal", "0"),
            actividad.get("lugar", ""),
            actividad.get("comentarios", "")
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar la actividad: {e}")
        return False

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
    try:
        datos = cargar_datos()
        if 0 <= indice < len(datos):
            id_actividad = datos[indice]["id"]
            conn = database.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM actividades WHERE id = ?", (id_actividad,))
            conn.commit()
            conn.close()
            return True
        return False
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar la actividad: {e}")
        return False

def editar_actividad(indice, nueva_actividad):
    """Edita una actividad por su índice (posición en lista)"""
    try:
        datos = cargar_datos()
        if 0 <= indice < len(datos):
            id_actividad = datos[indice]["id"]
            conn = database.conectar()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE actividades SET
                tipo = ?, fecha = ?, inicio = ?, fin = ?, duracion_min = ?,
                distancia_km = ?, calorias_kcal = ?, lugar = ?, comentarios = ?
                WHERE id = ?
            ''', (
                nueva_actividad.get("tipo", ""),
                nueva_actividad.get("fecha", ""),
                nueva_actividad.get("inicio", ""),
                nueva_actividad.get("fin", ""),
                nueva_actividad.get("duracion_min", "0"),
                nueva_actividad.get("distancia_km", "0"),
                nueva_actividad.get("calorias_kcal", "0"),
                nueva_actividad.get("lugar", ""),
                nueva_actividad.get("comentarios", ""),
                id_actividad
            ))
            conn.commit()
            conn.close()
            return True
        return False
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo editar la actividad: {e}")
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