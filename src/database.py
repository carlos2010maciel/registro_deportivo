# src/database.py
import sqlite3
import os

# Ruta dinámica a la base de datos
directorio_actual = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(directorio_actual, "..", "data", "registro.db")

def conectar():
    """Conecta a la base de datos y crea la tabla si no existe"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS actividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            fecha TEXT NOT NULL,
            inicio TEXT,
            fin TEXT,
            duracion_min TEXT,
            distancia_km TEXT,
            calorias_kcal TEXT,
            lugar TEXT,
            comentarios TEXT
        )
    ''')
    conn.commit()
    return conn