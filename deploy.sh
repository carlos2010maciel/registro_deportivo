#!/bin/bash

echo "🚀 Iniciando build y deploy automático..."

# Paso 1: Ejecutar el build
if [ ! -f "build.sh" ]; then
    echo "❌ No se encontró build.sh"
    exit 1
fi

./build.sh
if [ $? -ne 0 ]; then
    echo "❌ Error en el proceso de build"
    exit 1
fi

# Paso 2: Crear carpeta de release
mkdir -p release
cp dist/RegistroDeportivo release/RegistroDeportivo-$(date +%Y%m%d)
echo "✅ Ejecutable copiado a release/"

# Paso 3: Sincronizar código con GitHub (solo código, no binarios)
git add .
git commit -m "📦 Build automático: $(date '+%Y-%m-%d %H:%M')" --only
git push origin main

echo "🎉 Build y deploy completado!"
echo "➡️  Ejecutable listo en: release/"
echo "☁️  Código sincronizado con GitHub"