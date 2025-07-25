#!/bin/bash

# deploy.sh - Genera una carpeta portable lista para USB
# Ejecutar: ./deploy.sh [--auto]
# Opciones: --auto (no pregunta nada, útil para CI/CD)

# =============================
# PARÁMETROS Y MODO AUTOMÁTICO
# =============================
AUTO_MODE=false
for arg in "$@"; do
  if [ "$arg" = "--auto" ]; then
    AUTO_MODE=true
  fi
done

echo "🚀 Iniciando despliegue de versión portable..."

# =============================
# DETECCIÓN DE PLATAFORMA
# =============================
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="linux"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    PLATFORM="windows"
else
    PLATFORM="unknown"
fi
echo "🖥️  Plataforma detectada: $PLATFORM"

# =============================
# ARCHIVO DE VERSIÓN
# =============================
VERSION_FILE="version.txt"
DEFAULT_VERSION="1.0.0"

# Si no existe, crear con versión por defecto
if [ ! -f "$VERSION_FILE" ]; then
    echo "$DEFAULT_VERSION" > "$VERSION_FILE"
    echo "🆕 Archivo de versión creado: $VERSION_FILE con $DEFAULT_VERSION"
fi

# Leer versión actual
CURRENT_VERSION=$(cat "$VERSION_FILE" | tr -d ' \t\n\r')
if [[ ! "$CURRENT_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "❌ Formato de versión inválido en $VERSION_FILE: '$CURRENT_VERSION'"
    echo "🔧 Usando versión por defecto: $DEFAULT_VERSION"
    CURRENT_VERSION="$DEFAULT_VERSION"
    echo "$DEFAULT_VERSION" > "$VERSION_FILE"
fi

# Descomponer versión
MAJOR=$(echo "$CURRENT_VERSION" | cut -d. -f1)
MINOR=$(echo "$CURRENT_VERSION" | cut -d. -f2)
PATCH=$(echo "$CURRENT_VERSION" | cut -d. -f3)

# Incrementar parche (por defecto)
NEW_PATCH=$((PATCH + 1))
NEW_VERSION="$MAJOR.$MINOR.$NEW_PATCH"

# Preguntar al usuario si NO está en modo automático
if [ "$AUTO_MODE" = false ]; then
    echo "📦 Versión actual: v$CURRENT_VERSION"
    echo "   ¿Qué tipo de versión deseas crear?"
    echo "   1) Parche (recomendado)  : v$MAJOR.$MINOR.$PATCH → v$NEW_VERSION"
    echo "   2) Menor (nueva función)  : v$MAJOR.$MINOR.$PATCH → v$MAJOR.$((MINOR + 1)).0"
    echo "   3) Mayor (cambio grande)  : v$MAJOR.$MINOR.$PATCH → v$((MAJOR + 1)).0.0"
    read -p "Selecciona (1/2/3) [1]: " choice
else
    echo "⚙️  Modo automático activado. Incrementando parche."
    choice="1"
fi

case "$choice" in
    2)
        NEW_VERSION="$MAJOR.$((MINOR + 1)).0"
        ;;
    3)
        NEW_VERSION="$((MAJOR + 1)).0.0"
        ;;
    ""|1)
        # Usa NEW_VERSION ya calculado (parche)
        ;;
    *)
        echo "Opción inválida. Usando parche."
        ;;
esac

# Guardar nueva versión
echo "$NEW_VERSION" > "$VERSION_FILE"
echo "🔖 Nueva versión: v$NEW_VERSION (guardada en $VERSION_FILE)"

# =============================
# CONTADOR DE BUILDS DEL DÍA
# =============================
DATE=$(date +%Y%m%d)
BUILD_COUNT_FILE="build_counter.txt"

if [ -f "$BUILD_COUNT_FILE" ]; then
    LAST_DATE=$(head -n1 "$BUILD_COUNT_FILE" | cut -d' ' -f1)
    COUNTER=$(head -n1 "$BUILD_COUNT_FILE" | cut -d' ' -f2)
else
    LAST_DATE=""
    COUNTER=0
fi

if [ "$LAST_DATE" != "$DATE" ]; then
    COUNTER=1
else
    COUNTER=$((COUNTER + 1))
fi

echo "$DATE $COUNTER" > "$BUILD_COUNT_FILE"

# Construir versión completa
FULL_VERSION="${NEW_VERSION}-${DATE}.${COUNTER}"
echo "📦 Versión de build: v${FULL_VERSION}"

# =============================
# VARIABLES
# =============================
APP_NAME="RegistroDeportivo"
OUTPUT_DIR="release/${APP_NAME}_Portable_v${NEW_VERSION}_${PLATFORM}"
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
# PASO 3: Script de inicio (Linux y Windows)
# =============================

# --- Linux: iniciar.sh ---
cat > "$OUTPUT_DIR/iniciar.sh" << 'EOF'
#!/bin/bash
echo "🚀 Iniciando Registro Deportivo..."
chmod +x "$0"
BASEDIR=$(dirname "$0")
cd "$BASEDIR"
./RegistroDeportivo
EOF
chmod +x "$OUTPUT_DIR/iniciar.sh"
echo "✅ Script de inicio para Linux: iniciar.sh"

# --- Windows: iniciar.bat ---
cat > "$OUTPUT_DIR/iniciar.bat" << EOF
@echo off
echo 🚀 Iniciando Registro Deportivo...
RegistroDeportivo.exe
pause
EOF
echo "✅ Script de inicio para Windows: iniciar.bat"

# =============================
# PASO 4: Generar CHANGELOG.txt
# =============================
CHANGELOG_FILE="CHANGELOG.txt"
BACKUP_FILE="changelog_backup.txt"

# Hacer copia de seguridad si existe
if [ -f "$CHANGELOG_FILE" ]; then
    cp "$CHANGELOG_FILE" "$BACKUP_FILE"
fi

# Crear nuevo encabezado
cat > "$OUTPUT_DIR/CHANGELOG.txt" << EOF
# Registro Deportivo - Historial de cambios

## v${NEW_VERSION} - $(date '+%Y-%m-%d')
- Build automático: v${FULL_VERSION}
- Plataforma: ${PLATFORM}
- Cambio: Incremento de versión

### Notas
Este archivo registra las versiones generadas.
Para ver cambios específicos, revisa el repositorio o el archivo de respaldo.

Generado automáticamente por deploy.sh
EOF

echo "✅ CHANGELOG.txt generado en el release"

# Restaurar backup al final (opcional)
if [ -f "$BACKUP_FILE" ]; then
    cat "$BACKUP_FILE" >> "$OUTPUT_DIR/CHANGELOG.txt"
    rm "$BACKUP_FILE"
fi

# =============================
# PASO 5: Crear README.txt
# =============================
cat > "$OUTPUT_DIR/README.txt" << EOF
========================================
       REGISTRO DEPORTIVO - USB
========================================

Aplicación portable para registrar tus actividades:
- Caminata, Running, Trail, Ciclismo, etc.

No requiere instalación. Solo ejecútala desde esta carpeta.

Versión: v${NEW_VERSION}
Plataforma: ${PLATFORM}
Build: v${FULL_VERSION}
Creado el: $(date '+%Y-%m-%d %H:%M')

========================================
       CÓMO USARLO EN ${PLATFORM^^}
========================================

Linux:
  - Abre terminal → ./iniciar.sh

Windows:
  - Haz doble clic en 'iniciar.bat'

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
- Linux: python3-tk (sudo apt install python3-tk)
- Windows: compatible con 64 bits

¡Listo! Disfruta tu registro deportivo portable.
EOF

echo "✅ Archivo README.txt creado"

# =============================
# PASO 6: Comprimir en .zip
# =============================
ZIP_NAME="${OUTPUT_DIR}.zip"
cd release
echo "📦 Comprimiendo en $ZIP_NAME..."
zip -r "$ZIP_NAME" "$(basename "$OUTPUT_DIR")" > /dev/null
cd ..
echo "✅ Release comprimido: $ZIP_NAME"

# =============================
# RESUMEN FINAL
# =============================
echo ""
echo "🎉 ¡Despliegue completado!"
echo "📦 Carpeta portable: $OUTPUT_DIR/"
echo "📦 Archivo ZIP: $ZIP_NAME"
echo "🔖 Versión: v${NEW_VERSION}"
echo "🖥️  Plataforma: $PLATFORM"
echo "📋 Build: v${FULL_VERSION}"
echo ""
echo "📌 Puedes copiar la carpeta o el ZIP a una USB."
echo "💡 En Linux: ./iniciar.sh | En Windows: iniciar.bat"

# Abrir la carpeta (opcional)
if command -v xdg-open > /dev/null && [ "$PLATFORM" = "linux" ]; then
    xdg-open "release/"
fi