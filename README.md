# 🏃‍♂️ Registro Deportivo

Aplicación portable para registrar actividades deportivas: caminata, running, trail running, ciclismo de montaña y más.

Desarrollada en Python con interfaz gráfica (Tkinter) y almacenamiento local (SQLite), es ideal para llevar en una memoria USB y usarla en cualquier computadora con Linux o Windows, sin necesidad de instalación.

---

## ✅ Características

- Interfaz gráfica fácil de usar
- Registro de actividades con: tipo, fecha, hora de inicio/fin, duración, distancia, calorías, lugar y comentarios
- Edición y eliminación de actividades
- Estadísticas por tipo de actividad
- Almacenamiento seguro con SQLite
- Totalmente portable: todo en una carpeta
- Funciona sin internet ni instalación

---

## 🚀 Cómo ejecutar (modo desarrollo)

1. Abre una terminal en la carpeta del proyecto.
2. Crea y activa el entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Linux
   # venv\Scripts\activate      # Windows

3. Instala las dependencias
    pip install -r requirements.txt

4. Ejecuta la app
    python main.py

## Cómo generar el ejecutable portable (Linux)

1. Ejecuta el script de empaquetado:
    ./build.sh      # Se generará un archivo en dist/RegistroDeportivo.

## Cómo usar desde una memoria USB

1. Copia esta estructura a tu USB

    RegistroDeportivo_USB/
    ├── RegistroDeportivo
    ├── data/
    │   └── registro.db
    └── README.txt

2. En cualquier computadora con Linux:
    
    Conecta la USB
    Abre una terminal en la carpeta
    Da permisos (si es necesario):
        chmod +x RegistroDeportivo
    Ejecuta
        ./RegistroDeportivo     # Los datos se guardan automáticamente en data/registro.db

## ▶️ Cómo ejecutar el programa empaquetado
    Linux : ./RegistroDeportivo
    Windows : Haz doble clic en RegistroDeportivo.exe
    "La primera ejecución puede tardar unos segundos."

## Notas
    No subas venv/, dist/ ni registro.db a GitHub (están en .gitignore).
    Haz copias de seguridad de tu base de datos si es importante.
    Este proyecto está pensado para uso personal y desarrollo.

## Autor: Horacio Carlos Maciel de Lima
    https://github.com/carlos2010maciel
    https://www.linkedin.com/in/horacio-carlos-maciel-de-lima/