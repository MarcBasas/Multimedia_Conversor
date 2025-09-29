"""
Script para limpiar archivos temporales generados por PyInstaller
"""
import os
import shutil


def clean_build_files():
    """Elimina archivos y carpetas temporales"""
    
    files_to_remove = [
        "build",
        "ConversorMultimedia.spec",
        "__pycache__"
    ]
    
    removed_count = 0
    
    for item in files_to_remove:
        if os.path.exists(item):
            try:
                if os.path.isdir(item):
                    shutil.rmtree(item)
                    print(f"Eliminada carpeta: {item}")
                else:
                    os.remove(item)
                    print(f"Eliminado archivo: {item}")
                removed_count += 1
            except Exception as e:
                print(f"Error eliminando {item}: {e}")
    
    if removed_count == 0:
        print("No hay archivos temporales para limpiar")
    else:
        print(f"Limpieza completada. {removed_count} elementos eliminados.")


if __name__ == "__main__":
    clean_build_files()
