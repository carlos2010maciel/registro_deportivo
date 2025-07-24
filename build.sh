#!/bin/bash

# Script de empaquetado para Registro Deportivo
# Ejecutar en Parrot OS con entorno virtual

echo "🚀 Iniciando proceso de empaquetado..."

# Nombre del entorno virtual
VENV_DIR="venv"

# Verificar si existe el entorno virtual, si no, crearlo
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv $VENV_DIR
    if [ $? -ne 0 ]; then
        echo "❌ Error al crear el entorno virtual. Asegúrate de tener 'python3-venv' instalado."
        echo "   Ejecuta: sudo apt install python3-venv"
        exit 1
    fi
fi

# Activar el entorno virtual
echo "⚡ Activando entorno virtual..."
source $VENV_DIR/bin/activate

# Verificar si pyinstaller está instalado
if ! python -m pyinstaller --version > /dev/null 2>&1; then
    echo "📥 Instalando PyInstaller..."
    pip install pyinstaller > /dev/null
    if [ $? -ne 0 ]; then
        echo "❌ Error al instalar PyInstaller."
        exit 1
    fi
fi

# Mostrar versión de PyInstaller
echo "✅ PyInstaller instalado."
pyinstaller --version

# Crear carpeta dist si no existe
mkdir -p dist

# Ejecutar PyInstaller
echo "📦 Empaquetando main.py..."
pyinstaller \
    --onefile \
    --windowed \
    --name "RegistroDeportivo" \
    --add-data "data:data" \
    main.py

# Verificar si el empaquetado fue exitoso
if [ -f "dist/RegistroDeportivo" ]; then
    echo "🎉 ¡Éxito! Ejecutable creado: dist/RegistroDeportivo"
    echo "💡 Puedes copiarlo a una USB y ejecutarlo en otras máquinas con Linux."
else
    echo "❌ Error: No se generó el ejecutable."
    exit 1
fi

# Opcional: limpiar archivos temporales (descomenta si quieres)
echo "🧹 Limpiando archivos temporales..."
rm -rf build/ main.spec

echo "✅ Proceso de empaquetado finalizado."