# Conversor Multimedia

Aplicación para convertir imágenes, videos y audio entre diferentes formatos.

## Descarga

**[Descargar ConversorMultimedia.exe](https://github.com/MarcBasas/Multimedia_Conversor/releases/tag/v1.0.0)**

No necesitas instalar Python ni dependencias adicionales. Solo descarga y ejecuta.

## Características

**Imágenes:** JPEG, PNG, WEBP, BMP, TIFF, GIF
**Video:** MP4, AVI, MOV, MKV, WEBM, FLV, **GIF** (desde video)
**Audio:** MP3, WAV, FLAC, AAC, OGG, M4A

- Conversión por lotes
- Control de calidad y bitrate
- Redimensionado opcional
- **Conversión de video a GIF** con opciones avanzadas
- Interfaz simple e intuitiva

## Como usar

1. **Ejecuta** ConversorMultimedia.exe
2. **Selecciona el tipo** de archivo: Imágenes, Video o Audio
3. **Elige los archivos** que quieres convertir
4. **Selecciona el formato** de salida
5. **Configura opciones** (calidad, bitrate, etc.)
6. **Haz clic en Convertir**

Los archivos convertidos se guardan con "_converted" en el nombre.

## ✨ Conversión Video a GIF

Cuando selecciones **Video** como tipo de archivo y **GIF** como formato de salida, tendrás opciones especiales:

- **GIF FPS:** Controla la velocidad del GIF (5-30 fps recomendado)
- **Duración:** Especifica cuántos segundos convertir (vacío = video completo)
- **Optimizar GIF:** Reduce el tamaño del archivo resultante
- **Redimensionar:** Ajusta las dimensiones para GIFs más pequeños

💡 **Consejos para mejores GIFs:**
- Usa 10-15 FPS para un buen balance calidad/tamaño
- Redimensiona a 480px o menos para archivos más pequeños
- Limita la duración a 3-10 segundos para GIFs web

## Formatos soportados

| Tipo | Formatos de entrada | Formatos de salida |
|------|--------------------|--------------------|
| **Imágenes** | JPEG, PNG, BMP, GIF, TIFF, WEBP | JPEG, PNG, WEBP, BMP, TIFF, GIF |
| **Video** | MP4, AVI, MOV, MKV, WEBM, FLV, WMV, M4V | MP4, AVI, MOV, MKV, WEBM, FLV, **GIF** |
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
```

### 🔨 Crear ejecutables

#### Método automático (recomendado):

**Windows:**
```cmd
build_windows.bat
```

**macOS:**
```bash
chmod +x build_mac.sh
./build_mac.sh
```

**Linux:**
```bash
cd src && python build_exe.py
```

#### Método manual:
```bash
# Desde la carpeta src
cd src
python build_exe.py
```

El script detecta automáticamente tu plataforma y crea el ejecutable apropiado:
- **Windows**: `ConversorMultimedia.exe`
- **macOS**: `ConversorMultimedia.app` 
- **Linux**: `ConversorMultimedia`

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
