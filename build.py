# build.py
import os
import sys
from PyInstaller.__main__ import run

# Configuración del build
spec = [
    'main.py',
    '--name=RegistroDeportivo',
    '--windowed',           # Sin consola (solo GUI)
    '--onefile',            # Un solo archivo .exe o binario
    '--clean',
    '--add-data=data;data'  # Incluye la carpeta data (Windows usa ;, Linux usa :)
]

# Ajustar separador según el sistema
if sys.platform.startswith('linux'):
    spec[-1] = '--add-data=data:data'

run(spec)