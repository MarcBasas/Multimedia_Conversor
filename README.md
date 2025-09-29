# Conversor Multimedia

Aplicación para convertir imágenes, videos y audio entre diferentes formatos.

## Descarga

**[Descargar ConversorMultimedia.exe]([https://github.com/MarcBasas/Multimedia_Conversor/releases/tag/v1.0.0])**

No necesitas instalar Python ni dependencias adicionales. Solo descarga y ejecuta.

## Características

**Imágenes:** JPEG, PNG, WEBP, BMP, TIFF, GIF
**Video:** MP4, AVI, MOV, MKV, WEBM, FLV  
**Audio:** MP3, WAV, FLAC, AAC, OGG, M4A

- Conversión por lotes
- Control de calidad y bitrate
- Redimensionado opcional
- Interfaz simple e intuitiva

## Como usar

1. **Ejecuta** ConversorMultimedia.exe
2. **Selecciona el tipo** de archivo: Imágenes, Video o Audio
3. **Elige los archivos** que quieres convertir
4. **Selecciona el formato** de salida
5. **Configura opciones** (calidad, bitrate, etc.)
6. **Haz clic en Convertir**

Los archivos convertidos se guardan con "_converted" en el nombre.

## Formatos soportados

| Tipo | Formatos de entrada | Formatos de salida |
|------|--------------------|--------------------|
| **Imágenes** | JPEG, PNG, BMP, GIF, TIFF, WEBP | JPEG, PNG, WEBP, BMP, TIFF, GIF |
| **Video** | MP4, AVI, MOV, MKV, WEBM, FLV, WMV, M4V | MP4, AVI, MOV, MKV, WEBM, FLV |
| **Audio** | MP3, WAV, FLAC, AAC, OGG, M4A, WMA | MP3, WAV, FLAC, AAC, OGG, M4A |

## Para desarrolladores

Si quieres modificar el código o compilar tu propio ejecutable:

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/conversor-multimedia.git
cd conversor-multimedia

# Instalar dependencias
pip install -r src/requirements.txt

# Ejecutar desde código
python src/multimedia_converter.py

# Crear ejecutable (desde la carpeta src)
cd src
python build_exe.py
```

**Estructura del proyecto:**
```
conversor-multimedia/
├── README.md                    # Este archivo
├── LICENSE                      # Licencia MIT
├── .gitignore                  # Archivos a ignorar
├── dist/                       # Ejecutables (no en git)
│   └── ConversorMultimedia.exe
└── src/                        # Código fuente
    ├── multimedia_converter.py # Aplicación principal
    ├── build_exe.py            # Crear ejecutable
    ├── clean.py                # Limpiar archivos temporales
    └── requirements.txt        # Dependencias
```

## Licencia

Proyecto de uso libre para fines educativos y personales.
