#!/bin/bash
# Script para crear ejecutable en macOS

echo "🍎 Creando ejecutable para macOS..."

# Verificar que estamos en macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Este script solo funciona en macOS"
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install -r src/requirements.txt

# Crear ejecutable
echo "🔨 Construyendo ejecutable..."
cd src
python build_exe.py

echo "✅ ¡Ejecutable creado!"
echo "📁 Ubicación: dist/ConversorMultimedia.app"
echo ""
echo "Para ejecutar:"
echo "  open dist/ConversorMultimedia.app"
