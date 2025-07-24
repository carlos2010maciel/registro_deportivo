#!/bin/bash

# deploy.sh - Genera una carpeta portable lista para USB
# Ejecutar: ./deploy.sh

echo "🚀 Iniciando despliegue de versión portable..."

# Variables
APP_NAME="RegistroDeportivo"
VERSION=$(date +%Y%m%d)
OUTPUT_DIR="release/${APP_NAME}_Portable_${VERSION}"
EXECUTABLE="dist/${APP_NAME}"

# Paso 1: Ejecutar build.sh para generar el ejecutable
if [ ! -f "build.sh" ]; then
    echo "❌ No se encontró build.sh"
    exit 1
fi

./build.sh
if [ $? -ne 0 ]; then
    echo "❌ Error en el build. Abortando."
    exit 1
fi

# Paso 2: Crear carpeta portable
echo "📁 Creando carpeta portable..."
rm -rf "$OUTPUT_DIR"  # Limpiar versión anterior
mkdir -p "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/data"

# Copiar ejecutable
if [ -f "$EXECUTABLE" ]; then
    cp "$EXECUTABLE" "$OUTPUT_DIR/"
    echo "✅ Ejecutable copiado"
else
    echo "❌ No se generó el ejecutable"
    exit 1
fi

# Crear data vacía (para que guarde los datos del usuario)
touch "$OUTPUT_DIR/data/.gitkeep"  # Solo para mantener la estructura si usas Git

# Crear script de inicio para Linux
cat > "$OUTPUT_DIR/iniciar.sh" << 'EOF'
#!/bin/bash
# Script para iniciar la app desde cualquier lugar

echo "🚀 Iniciando Registro Deportivo..."
echo "ℹ️  Asegúrate de tener permisos de ejecución."
echo "⏳ Esperando..."

# Hacer ejecutable (por si acaso)
chmod +x "$0"
BASEDIR=$(dirname "$0")
cd "$BASEDIR"

# Ejecutar
./RegistroDeportivo

if [ $? -ne 0 ]; then
    echo "❌ Error al iniciar la aplicación."
    echo "💡 Asegúrate de tener instalado: python3-tk"
    read -p "Presiona Enter para salir..."
fi
EOF

chmod +x "$OUTPUT_DIR/iniciar.sh"
echo "✅ Script de inicio creado: iniciar.sh"

# Crear README
cat > "$OUTPUT_DIR/README.txt" << EOF
Registro Deportivo - Versión Portable

Instrucciones:
1. Copia esta carpeta a una USB o disco externo.
2. Haz doble clic en 'iniciar.sh' para ejecutar.
   - En algunos sistemas, debes hacer clic derecho → "Ejecutar en terminal"
3. Registra tus actividades: running, ciclismo, etc.
4. Tus datos se guardan en la carpeta 'data/'.

Requisitos:
- Sistema Linux (Parrot, Ubuntu, etc.)
- Tener instalado 'python3-tk' (si falla, ejecuta: sudo apt install python3-tk)

Creado el: $(date '+%Y-%m-%d')
EOF

echo "✅ Archivo README.txt creado"

# Resumen final
echo ""
echo "🎉 ¡Despliegue completado!"
echo "📦 Carpeta portable lista en:"
echo "   $OUTPUT_DIR/"
echo ""
echo "📌 Puedes copiarla directamente a una USB y usarla en cualquier PC con Linux."
echo "💡 Para usar: haz clic en 'iniciar.sh' (puede necesitar permisos de ejecución)."

# Abrir la carpeta (opcional)
if command -v xdg-open > /dev/null; then
    xdg-open "$OUTPUT_DIR"
fi