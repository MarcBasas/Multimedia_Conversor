# Guía para Desarrolladores

## Archivos del proyecto

- **`multimedia_converter.py`** - Aplicación principal con interfaz gráfica
- **`build_exe.py`** - Script para crear ejecutable con PyInstaller
- **`clean.py`** - Utilidad para limpiar archivos temporales
- **`requirements.txt`** - Dependencias de Python

## Desarrollo

### Ejecutar desde código
```bash
# Desde la raíz del proyecto
python src/multimedia_converter.py
```

### Crear ejecutable
```bash
cd src
python build_exe.py
```

### Limpiar archivos temporales
```bash
cd src
python clean.py
```

## Dependencias

- **Pillow** - Procesamiento de imágenes
- **MoviePy** - Conversión de video (requiere FFmpeg)
- **Pydub** - Procesamiento de audio
- **PyInstaller** - Creación de ejecutables

## Estructura de la aplicación

La aplicación usa una interfaz dinámica que cambia según el tipo de archivo seleccionado:
- **Imágenes**: Pillow para conversión y redimensionado
- **Video**: MoviePy para conversión con control de bitrate y FPS
- **Audio**: Pydub para conversión con control de bitrate y sample rate

## Notas técnicas

- La interfaz se actualiza dinámicamente usando `update_format_options()`
- Las conversiones se ejecutan en hilos separados para no bloquear la UI
- Los archivos convertidos se guardan con sufijo "_converted"
- Se incluyen importaciones condicionales para dependencias opcionales
