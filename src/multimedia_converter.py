import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import threading
from pathlib import Path
import subprocess

# Importaciones condicionales para multimedia
try:
    from moviepy.editor import VideoFileClip, AudioFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False


class MultimediaConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor Multimedia - Imágenes, Video y Audio")
        self.root.geometry("700x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.selected_files = []
        self.file_type = tk.StringVar(value="image")  # image, video, audio
        self.output_format = tk.StringVar(value="JPEG")
        self.output_quality = tk.IntVar(value=95)
        self.resize_enabled = tk.BooleanVar(value=False)
        self.resize_width = tk.IntVar(value=800)
        self.resize_height = tk.IntVar(value=600)
        self.maintain_aspect = tk.BooleanVar(value=True)
        
        # Variables específicas para video
        self.video_bitrate = tk.StringVar(value="1000k")
        self.video_fps = tk.IntVar(value=30)
        self.video_codec = tk.StringVar(value="libx264")
        
        # Variables específicas para audio
        self.audio_bitrate = tk.StringVar(value="128k")
        self.audio_sample_rate = tk.IntVar(value=44100)
        
        self.output_folder = None
        self.setup_ui()
        self.update_format_options()
    
    def setup_ui(self):
        # Título
        title_label = tk.Label(
            self.root, 
            text="Conversor Multimedia", 
            font=("Arial", 18, "bold"),
            bg='#f0f0f0',
            fg='#333'
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            self.root, 
            text="Imágenes • Video • Audio", 
            font=("Arial", 12),
            bg='#f0f0f0',
            fg='#666'
        )
        subtitle_label.pack(pady=(0, 15))
        
        # Frame para tipo de archivo
        type_frame = tk.LabelFrame(
            self.root,
            text="Tipo de Archivo",
            bg='#f0f0f0',
            fg='#333',
            font=("Arial", 10, "bold")
        )
        type_frame.pack(pady=10, padx=20, fill='x')
        
        type_options = [
            ("Imágenes", "image"),
            ("Video", "video"),
            ("Audio", "audio")
        ]
        
        for text, value in type_options:
            tk.Radiobutton(
                type_frame,
                text=text,
                variable=self.file_type,
                value=value,
                bg='#f0f0f0',
                fg='#333',
                command=self.update_format_options,
                font=("Arial", 10)
            ).pack(side='left', padx=15, pady=5)
        
        # Frame para selección de archivos
        file_frame = tk.Frame(self.root, bg='#f0f0f0')
        file_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Button(
            file_frame,
            text="Seleccionar Archivos",
            command=self.select_files,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        ).pack(side='left')
        
        self.files_label = tk.Label(
            file_frame,
            text="No hay archivos seleccionados",
            bg='#f0f0f0',
            fg='#666'
        )
        self.files_label.pack(side='left', padx=(10, 0))
        
        # Frame para opciones de formato (dinámico)
        self.format_frame = tk.LabelFrame(
            self.root,
            text="Formato de Salida",
            bg='#f0f0f0',
            fg='#333',
            font=("Arial", 10, "bold")
        )
        self.format_frame.pack(pady=10, padx=20, fill='x')
        
        # Frame para opciones específicas (dinámico)
        self.options_frame = tk.LabelFrame(
            self.root,
            text="Opciones",
            bg='#f0f0f0',
            fg='#333',
            font=("Arial", 10, "bold")
        )
        self.options_frame.pack(pady=10, padx=20, fill='x')
        
        # Frame para directorio de salida
        output_frame = tk.Frame(self.root, bg='#f0f0f0')
        output_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Button(
            output_frame,
            text="Carpeta de Destino",
            command=self.select_output_folder,
            bg='#2196F3',
            fg='white',
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        ).pack(side='left')
        
        self.output_label = tk.Label(
            output_frame,
            text="Misma carpeta que archivos originales",
            bg='#f0f0f0',
            fg='#666'
        )
        self.output_label.pack(side='left', padx=(10, 0))
        
        # Botón de conversión
        tk.Button(
            self.root,
            text="Convertir Archivos",
            command=self.convert_files,
            bg='#FF9800',
            fg='white',
            font=("Arial", 12, "bold"),
            padx=30,
            pady=10
        ).pack(pady=20)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(
            self.root,
            mode='determinate',
            length=500
        )
        self.progress.pack(pady=10)
        
        self.status_label = tk.Label(
            self.root,
            text="Listo para convertir",
            bg='#f0f0f0',
            fg='#333'
        )
        self.status_label.pack()
        
        # Información de dependencias
        info_text = "    "
        if not MOVIEPY_AVAILABLE:
            info_text += "Video: Instalar moviepy | "
        if not PYDUB_AVAILABLE:
            info_text += "Audio: Instalar pydub | "
        if info_text == "   ":
            info_text += "Todas las funciones disponibles"
        else:
            info_text = info_text.rstrip(" | ")
        
        info_label = tk.Label(
            self.root,
            text=info_text,
            bg='#f0f0f0',
            fg='#888',
            font=("Arial", 8)
        )
        info_label.pack(pady=(10, 5))
    
    def update_format_options(self):
        # Limpiar frames
        for widget in self.format_frame.winfo_children():
            widget.destroy()
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        file_type = self.file_type.get()
        
        if file_type == "image":
            self.setup_image_options()
        elif file_type == "video":
            self.setup_video_options()
        elif file_type == "audio":
            self.setup_audio_options()
    
    def setup_image_options(self):
        # Formatos de imagen
        formats = ["JPEG", "PNG", "WEBP", "BMP", "TIFF", "GIF"]
        self.output_format.set("JPEG")
        
        for fmt in formats:
            tk.Radiobutton(
                self.format_frame,
                text=fmt,
                variable=self.output_format,
                value=fmt,
                bg='#f0f0f0',
                fg='#333'
            ).pack(side='left', padx=8, pady=5)
        
        # Opciones de imagen
        # Calidad
        quality_frame = tk.Frame(self.options_frame, bg='#f0f0f0')
        quality_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            quality_frame,
            text="Calidad (1-100):",
            bg='#f0f0f0',
            fg='#333'
        ).pack(side='left')
        
        tk.Scale(
            quality_frame,
            from_=1,
            to=100,
            orient='horizontal',
            variable=self.output_quality,
            bg='#f0f0f0',
            fg='#333',
            length=150
        ).pack(side='left', padx=10)
        
        # Redimensionado
        resize_frame = tk.Frame(self.options_frame, bg='#f0f0f0')
        resize_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Checkbutton(
            resize_frame,
            text="Redimensionar:",
            variable=self.resize_enabled,
            bg='#f0f0f0',
            fg='#333'
        ).pack(side='left')
        
        tk.Label(resize_frame, text="W:", bg='#f0f0f0', fg='#333').pack(side='left', padx=(10, 0))
        tk.Entry(resize_frame, textvariable=self.resize_width, width=6).pack(side='left', padx=2)
        tk.Label(resize_frame, text="H:", bg='#f0f0f0', fg='#333').pack(side='left', padx=(5, 0))
        tk.Entry(resize_frame, textvariable=self.resize_height, width=6).pack(side='left', padx=2)
        
        tk.Checkbutton(
            resize_frame,
            text="Mantener proporción",
            variable=self.maintain_aspect,
            bg='#f0f0f0',
            fg='#333'
        ).pack(side='left', padx=10)
    
    def setup_video_options(self):
        # Formatos de video
        formats = ["MP4", "AVI", "MOV", "MKV", "WEBM", "FLV"]
        self.output_format.set("MP4")
        
        for fmt in formats:
            tk.Radiobutton(
                self.format_frame,
                text=fmt,
                variable=self.output_format,
                value=fmt,
                bg='#f0f0f0',
                fg='#333'
            ).pack(side='left', padx=8, pady=5)
        
        # Opciones de video
        # Bitrate
        bitrate_frame = tk.Frame(self.options_frame, bg='#f0f0f0')
        bitrate_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(bitrate_frame, text="Bitrate:", bg='#f0f0f0', fg='#333').pack(side='left')
        bitrate_combo = ttk.Combobox(
            bitrate_frame,
            textvariable=self.video_bitrate,
            values=["500k", "1000k", "2000k", "4000k", "8000k"],
            width=8
        )
        bitrate_combo.pack(side='left', padx=5)
        
        # FPS
        tk.Label(bitrate_frame, text="FPS:", bg='#f0f0f0', fg='#333').pack(side='left', padx=(15, 0))
        fps_combo = ttk.Combobox(
            bitrate_frame,
            textvariable=self.video_fps,
            values=[24, 25, 30, 50, 60],
            width=6
        )
        fps_combo.pack(side='left', padx=5)
        
        # Redimensionado de video
        resize_frame = tk.Frame(self.options_frame, bg='#f0f0f0')
        resize_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Checkbutton(
            resize_frame,
            text="Redimensionar:",
            variable=self.resize_enabled,
            bg='#f0f0f0',
            fg='#333'
        ).pack(side='left')
        
        tk.Label(resize_frame, text="W:", bg='#f0f0f0', fg='#333').pack(side='left', padx=(10, 0))
        tk.Entry(resize_frame, textvariable=self.resize_width, width=6).pack(side='left', padx=2)
        tk.Label(resize_frame, text="H:", bg='#f0f0f0', fg='#333').pack(side='left', padx=(5, 0))
        tk.Entry(resize_frame, textvariable=self.resize_height, width=6).pack(side='left', padx=2)
    
    def setup_audio_options(self):
        # Formatos de audio
        formats = ["MP3", "WAV", "FLAC", "AAC", "OGG", "M4A"]
        self.output_format.set("MP3")
        
        for fmt in formats:
            tk.Radiobutton(
                self.format_frame,
                text=fmt,
                variable=self.output_format,
                value=fmt,
                bg='#f0f0f0',
                fg='#333'
            ).pack(side='left', padx=8, pady=5)
        
        # Opciones de audio
        audio_frame = tk.Frame(self.options_frame, bg='#f0f0f0')
        audio_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(audio_frame, text="Bitrate:", bg='#f0f0f0', fg='#333').pack(side='left')
        bitrate_combo = ttk.Combobox(
            audio_frame,
            textvariable=self.audio_bitrate,
            values=["64k", "128k", "192k", "256k", "320k"],
            width=8
        )
        bitrate_combo.pack(side='left', padx=5)
        
        tk.Label(audio_frame, text="Sample Rate:", bg='#f0f0f0', fg='#333').pack(side='left', padx=(15, 0))
        sample_combo = ttk.Combobox(
            audio_frame,
            textvariable=self.audio_sample_rate,
            values=[22050, 44100, 48000, 96000],
            width=8
        )
        sample_combo.pack(side='left', padx=5)
    
    def select_files(self):
        file_type = self.file_type.get()
        
        if file_type == "image":
            filetypes = [
                ("Imágenes", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp"),
                ("Todos los archivos", "*.*")
            ]
        elif file_type == "video":
            filetypes = [
                ("Videos", "*.mp4 *.avi *.mov *.mkv *.webm *.flv *.wmv *.m4v"),
                ("Todos los archivos", "*.*")
            ]
        else:  # audio
            filetypes = [
                ("Audio", "*.mp3 *.wav *.flac *.aac *.ogg *.m4a *.wma"),
                ("Todos los archivos", "*.*")
            ]
        
        files = filedialog.askopenfilenames(
            title=f"Seleccionar archivos de {file_type}",
            filetypes=filetypes
        )
        
        if files:
            self.selected_files = list(files)
            count = len(self.selected_files)
            self.files_label.config(
                text=f"{count} archivo{'s' if count != 1 else ''} seleccionado{'s' if count != 1 else ''}"
            )
    
    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Seleccionar carpeta de destino")
        if folder:
            self.output_folder = folder
            self.output_label.config(text=f"Destino: {os.path.basename(folder)}")
        else:
            self.output_folder = None
            self.output_label.config(text="Misma carpeta que archivos originales")
    
    def convert_files(self):
        if not self.selected_files:
            messagebox.showwarning("Advertencia", "Por favor, selecciona al menos un archivo.")
            return
        
        file_type = self.file_type.get()
        
        # Verificar dependencias
        if file_type == "video" and not MOVIEPY_AVAILABLE:
            messagebox.showerror("Error", "MoviePy no está instalado. Ejecuta: pip install moviepy")
            return
        
        if file_type == "audio" and not PYDUB_AVAILABLE:
            messagebox.showerror("Error", "Pydub no está instalado. Ejecuta: pip install pydub")
            return
        
        # Ejecutar conversión en hilo separado
        thread = threading.Thread(target=self._convert_worker)
        thread.daemon = True
        thread.start()
    
    def _convert_worker(self):
        total_files = len(self.selected_files)
        self.progress['maximum'] = total_files
        self.progress['value'] = 0
        
        converted_count = 0
        errors = []
        file_type = self.file_type.get()
        
        for i, file_path in enumerate(self.selected_files):
            try:
                self.status_label.config(text=f"Convirtiendo {os.path.basename(file_path)}...")
                self.root.update()
                
                if file_type == "image":
                    self._convert_image(file_path)
                elif file_type == "video":
                    self._convert_video(file_path)
                elif file_type == "audio":
                    self._convert_audio(file_path)
                
                converted_count += 1
                
            except Exception as e:
                errors.append(f"{os.path.basename(file_path)}: {str(e)}")
            
            # Actualizar progreso
            self.progress['value'] = i + 1
            self.root.update()
        
        # Mostrar resultados
        if errors:
            error_msg = f"Conversión completada con errores.\n\n"
            error_msg += f"Convertidos: {converted_count}/{total_files}\n\n"
            error_msg += "Errores:\n" + "\n".join(errors[:3])
            if len(errors) > 3:
                error_msg += f"\n... y {len(errors) - 3} errores más"
            messagebox.showwarning("Conversión completada con errores", error_msg)
        else:
            messagebox.showinfo(
                "Conversión completada",
                f"¡Todos los archivos se han convertido exitosamente!\n\n"
                f"Archivos convertidos: {converted_count}"
            )
        
        self.status_label.config(text="Conversión completada")
        self.progress['value'] = 0
    
    def _convert_image(self, file_path):
        """Convertir imagen usando Pillow"""
        with Image.open(file_path) as img:
            # Convertir a RGB si es necesario
            if self.output_format.get() == "JPEG" and img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Redimensionar si está habilitado
            if self.resize_enabled.get():
                width = self.resize_width.get()
                height = self.resize_height.get()
                
                if self.maintain_aspect.get():
                    img.thumbnail((width, height), Image.Resampling.LANCZOS)
                else:
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
            
            # Determinar ruta de salida
            output_path = self._get_output_path(file_path, self.output_format.get().lower())
            
            # Guardar imagen
            save_kwargs = {}
            if self.output_format.get() in ["JPEG", "WEBP"]:
                save_kwargs['quality'] = self.output_quality.get()
                save_kwargs['optimize'] = True
            
            img.save(output_path, format=self.output_format.get(), **save_kwargs)
    
    def _convert_video(self, file_path):
        """Convertir video usando MoviePy"""
        if not MOVIEPY_AVAILABLE:
            raise Exception("MoviePy no está disponible")
        
        with VideoFileClip(file_path) as video:
            # Redimensionar si está habilitado
            if self.resize_enabled.get():
                width = self.resize_width.get()
                height = self.resize_height.get()
                video = video.resize((width, height))
            
            # Cambiar FPS si es necesario
            if self.video_fps.get() != video.fps:
                video = video.set_fps(self.video_fps.get())
            
            # Determinar ruta de salida
            extension = self.output_format.get().lower()
            output_path = self._get_output_path(file_path, extension)
            
            # Configurar codec según formato
            codec_map = {
                'mp4': 'libx264',
                'avi': 'libxvid',
                'mov': 'libx264',
                'mkv': 'libx264',
                'webm': 'libvpx',
                'flv': 'flv'
            }
            
            codec = codec_map.get(extension, 'libx264')
            bitrate = self.video_bitrate.get()
            
            # Escribir video
            video.write_videofile(
                output_path,
                codec=codec,
                bitrate=bitrate,
                verbose=False,
                logger=None
            )
    
    def _convert_audio(self, file_path):
        """Convertir audio usando Pydub"""
        if not PYDUB_AVAILABLE:
            raise Exception("Pydub no está disponible")
        
        # Detectar formato de entrada
        input_format = Path(file_path).suffix[1:].lower()
        
        # Cargar audio
        audio = AudioSegment.from_file(file_path, format=input_format)
        
        # Cambiar sample rate si es necesario
        target_sample_rate = self.audio_sample_rate.get()
        if audio.frame_rate != target_sample_rate:
            audio = audio.set_frame_rate(target_sample_rate)
        
        # Determinar ruta de salida
        extension = self.output_format.get().lower()
        output_path = self._get_output_path(file_path, extension)
        
        # Configurar parámetros de exportación
        export_params = {}
        bitrate = self.audio_bitrate.get()
        
        if extension == "mp3":
            export_params = {"bitrate": bitrate}
        elif extension == "aac" or extension == "m4a":
            export_params = {"bitrate": bitrate}
        elif extension == "ogg":
            export_params = {"bitrate": bitrate}
        
        # Exportar audio
        audio.export(output_path, format=extension, **export_params)
    
    def _get_output_path(self, input_path, extension):
        """Generar ruta de salida para el archivo convertido"""
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        
        if extension == "jpeg":
            extension = "jpg"
        
        if self.output_folder:
            output_path = os.path.join(self.output_folder, f"{base_name}_converted.{extension}")
        else:
            output_dir = os.path.dirname(input_path)
            output_path = os.path.join(output_dir, f"{base_name}_converted.{extension}")
        
        return output_path


def main():
    root = tk.Tk()
    app = MultimediaConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
