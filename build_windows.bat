@echo off
REM Script para crear ejecutable en Windows

echo 🪟 Creando ejecutable para Windows...

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Instalar dependencias
echo 📥 Instalando dependencias...
python -m pip install --upgrade pip
pip install -r src\requirements.txt

REM Crear ejecutable
echo 🔨 Construyendo ejecutable...
cd src
python build_exe.py

echo ✅ ¡Ejecutable creado!
echo 📁 Ubicación: dist\ConversorMultimedia.exe
echo.
echo Para ejecutar:
echo   dist\ConversorMultimedia.exe

pause
