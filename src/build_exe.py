"""
Script para crear el ejecutable usando PyInstaller
Soporta Windows, macOS y Linux
"""
import os
import subprocess
import sys
import platform


def get_platform_config():
    """Obtiene la configuración específica de la plataforma"""
    system = platform.system().lower()
    
    if system == "windows":
        return {
            "windowed": True,
            "name": "ConversorMultimedia",
            "extension": ".exe"
        }
    elif system == "darwin":  # macOS
        return {
            "windowed": True,
            "name": "ConversorMultimedia",
            "extension": ""
        }
    else:  # Linux y otros
        return {
            "windowed": False,  # En Linux mejor con consola
            "name": "ConversorMultimedia",
            "extension": ""
        }


def build_executable():
    """Construye el ejecutable usando PyInstaller"""
    
    # Obtener configuración de plataforma
    config = get_platform_config()
    system = platform.system()
    
    # Comando base PyInstaller
    cmd = [
        "python", "-m", "PyInstaller",
        "--onefile",  # Un solo archivo ejecutable
        f"--name={config['name']}",  # Nombre del ejecutable
        "--clean",  # Limpiar cache
        "--hidden-import=moviepy.editor",  # Importación oculta para moviepy
        "--hidden-import=pydub",  # Importación oculta para pydub
        "--distpath=../dist",  # Carpeta de salida en la raíz
        "multimedia_converter.py"
    ]
    
    # Añadir --windowed solo si es necesario
    if config["windowed"]:
        cmd.insert(-1, "--windowed")  # Sin consola para Windows/Mac
    
    # Configuraciones específicas por plataforma
    if system == "Darwin":  # macOS
        cmd.extend([
            "--osx-bundle-identifier=com.conversor.multimedia",
            "--codesign-identity=-"  # Firma temporal para desarrollo
        ])
    # Para Windows no añadimos configuraciones adicionales por ahora
    
    try:
        print(f"Construyendo ejecutable para {system}...")
        print(f"Comando: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("OK Ejecutable creado exitosamente!")
        print(f"Ubicacion: dist/{config['name']}{config['extension']}")
        
        # Información específica por plataforma
        if system == "Darwin":
            print("\nPara macOS:")
            print("- Ejecutar desde terminal: ./ConversorMultimedia")
            print("- O hacer doble clic en Finder")
            print("- Para distribuir, considera firmar con certificado de desarrollador")
        elif system == "Windows":
            print("\nPara Windows:")
            print("- El archivo .exe se puede ejecutar directamente")
            print("- No requiere instalacion de Python")
        else:
            print("\nPara Linux:")
            print("- Ejecutar desde terminal: ./ConversorMultimedia")
            print("- Dar permisos de ejecucion: chmod +x ConversorMultimedia")
        
    except subprocess.CalledProcessError as e:
        print("ERROR: Error al crear el ejecutable:")
        print(e.stderr)
        return False
    
    except FileNotFoundError:
        print("ERROR: PyInstaller no esta instalado.")
        print("Instalalo con: pip install pyinstaller")
        return False
    
    return True


if __name__ == "__main__":
    build_executable()
