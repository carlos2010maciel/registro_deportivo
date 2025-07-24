#!/bin/bash

# deploy.sh - Genera una carpeta portable lista para USB
# Ejecutar: ./deploy.sh

echo "🚀 Iniciando despliegue de versión portable..."

# =============================
# CONFIGURACIÓN DE VERSIÓN
# =============================

# Versión semántica (cambia manualmente cuando añadas funciones)
SEMVER="1.0.0"

# Fecha actual en formato YYYYMMDD
DATE=$(date +%Y%m%d)

# Contador de builds del día: busca cuántos builds ya se hicieron hoy
BUILD_COUNT_FILE="build_counter.txt"
if [ -f "$BUILD_COUNT_FILE" ]; then
    LAST_DATE=$(head -n1 "$BUILD_COUNT_FILE" | cut -d' ' -f1)
    COUNTER=$(head -n1 "$BUILD_COUNT_FILE" | cut -d' ' -f2)
else
    LAST_DATE=""
    COUNTER=0
fi

# Reiniciar contador si es nuevo día
if [ "$LAST_DATE" != "$DATE" ]; then
    COUNTER=1
else
    COUNTER=$((COUNTER + 1))
fi

# Guardar contador
echo "$DATE $COUNTER" > "$BUILD_COUNT_FILE"

# Construir versión completa
VERSION="${SEMVER}-${DATE}.${COUNTER}"
echo "📦 Versión generada: v${VERSION}"

# =============================
# VARIABLES
# =============================
APP_NAME="RegistroDeportivo"
OUTPUT_DIR="release/${APP_NAME}_Portable_v${VERSION}"
EXECUTABLE="dist/${APP_NAME}"

# =============================
# PASO 1: Ejecutar build.sh
# =============================
if [ ! -f "build.sh" ]; then
    echo "❌ No se encontró build.sh"
    exit 1
fi

./build.sh
if [ $? -ne 0 ]; then
    echo "❌ Error en el build. Abortando."
    exit 1
fi

# =============================
# PASO 2: Crear carpeta portable
# =============================
echo "📁 Creando carpeta portable..."
rm -rf "$OUTPUT_DIR"
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

# Crear data vacía
touch "$OUTPUT_DIR/data/.gitkeep"

# =============================
# PASO 3: Script de inicio
# =============================
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

# =============================
# PASO 4: Crear README.txt
# =============================
cat > "$OUTPUT_DIR/README.txt" << EOF
========================================
       REGISTRO DEPORTIVO - USB
========================================

Aplicación portable para registrar tus actividades:
- Caminata, Running, Trail, Ciclismo, etc.

No requiere instalación. Solo ejecútala desde esta carpeta.

Versión: v${VERSION}
Creado el: $(date '+%Y-%m-%d %H:%M')

========================================
       CÓMO USARLO EN LINUX
========================================

1. Conecta esta USB a una computadora con Linux.

2. Abre una terminal en esta carpeta:
   - Haz clic derecho → "Abrir en terminal"

3. Da permiso de ejecución (solo la primera vez):
   chmod +x iniciar.sh

4. Ejecuta el programa:
   - Haz doble clic en 'iniciar.sh' o ejecútalo desde terminal.

✅ La primera vez puede tardar unos segundos.

========================================
       IMPORTANTE
========================================

- Los datos se guardan en la carpeta "data/"
- No elimines ni muevas la carpeta "data"
- Haz copias de seguridad de "data/registro.db"

========================================
       REQUISITOS
========================================
- Sistema Linux (Parrot, Ubuntu, etc.)
- Tener instalado 'python3-tk' (si falla: sudo apt install python3-tk)

¡Listo! Disfruta tu registro deportivo portable.
EOF

echo "✅ Archivo README.txt creado"

# =============================
# RESUMEN FINAL
# =============================
echo ""
echo "🎉 ¡Despliegue completado!"
echo "📦 Carpeta portable lista en:"
echo "   $OUTPUT_DIR/"
echo "🔖 Versión: v${VERSION}"
echo ""
echo "📌 Puedes copiarla directamente a una USB y usarla en cualquier PC con Linux."
echo "💡 Para usar: haz clic en 'iniciar.sh' (puede necesitar permisos de ejecución)."

# Abrir la carpeta (opcional)
if command -v xdg-open > /dev/null; then
    xdg-open "$OUTPUT_DIR"
fi