"""
Script para crear el ejecutable usando PyInstaller
"""
import os
import subprocess
import sys


def build_executable():
    """Construye el ejecutable usando PyInstaller"""
    
    # Comando PyInstaller usando módulo de Python
    cmd = [
        "python", "-m", "PyInstaller",
        "--onefile",  # Un solo archivo ejecutable
        "--windowed",  # Sin consola (solo para Windows)
        "--name=ConversorMultimedia",  # Nombre del ejecutable
        "--clean",  # Limpiar cache
        "--hidden-import=moviepy.editor",  # Importación oculta para moviepy
        "--hidden-import=pydub",  # Importación oculta para pydub
        "--distpath=../dist",  # Carpeta de salida en la raíz
        "multimedia_converter.py"
    ]
    
    try:
        print("Construyendo ejecutable...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Ejecutable creado exitosamente!")
        print("El ejecutable se encuentra en la carpeta 'dist/'")
        
    except subprocess.CalledProcessError as e:
        print("Error al crear el ejecutable:")
        print(e.stderr)
        return False
    
    except FileNotFoundError:
        print("PyInstaller no está instalado.")
        print("Instálalo con: pip install pyinstaller")
        return False
    
    return True


if __name__ == "__main__":
    build_executable()
