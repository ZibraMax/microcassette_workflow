# Audio Recorder & Transcriber with Phrase Detection

Este proyecto es un **script de grabación de audio** avanzado en Python que permite:

-   Grabar desde un micrófono seleccionado automáticamente por nombre.
-   Mostrar un **medidor de volumen en tiempo real** mientras se graba.
-   Detener la grabación automáticamente al escuchar una **frase clave** (“FIN DEL DIA”) o al presionar **ENTER**.
-   Reproducir un **beep de confirmación** cuando se detiene la grabación.
-   Guardar el audio final en **MP3**.
-   Generar una **transcripción completa** usando el modelo Whisper de OpenAI.

---

## 🛠️ Requisitos

Python >= 3.10 y las siguientes librerías:

```
sounddevice
numpy
scipy
ffmpeg-python
whisper
```

Asegúrate de tener **FFmpeg instalado** en tu sistema y accesible desde la terminal.

---

## 📦 Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/ZibraMax/microcassette_workflow
cd microcassette_workflow
```

2. Crear un entorno virtual (opcional pero recomendado):

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Uso

1. Ejecuta el script principal:

```bash
python main.py
```

2. Selecciona el micrófono **si coincide con KEYNAME** (por ejemplo `"BEHRINGER"`).
3. Presiona **ENTER** para comenzar a grabar.
4. Mientras se graba, verás un **medidor de volumen en tiempo real**.
5. La grabación se detendrá automáticamente si:

    - Detecta las frases en la variable STOP_PHRASES
    - Presionas **ENTER**

6. Al detenerse, se reproducirá un **beep de confirmación**.
7. Se generará un archivo **MP3** con el audio y un **TXT** con la transcripción.

---

## 🔧 Configuración

Dentro del script se pueden ajustar:

| Parámetro        | Descripción                                         |
| ---------------- | --------------------------------------------------- |
| `KEYNAME`        | Nombre parcial del micrófono a usar                 |
| `STOP_PHRASES`   | Frases que detienen la grabación                    |
| `BLOCK_DURATION` | Duración de cada bloque de audio para detección (s) |
| `BAR_LENGTH`     | Longitud de la barra del medidor de volumen         |
| `TIME_FORMAT`    | Formato de la carpeta de salida con timestamp       |

---

## 📂 Salida

-   Carpeta creada automáticamente con **timestamp**: `YYYYMMDD_HHMMSS`
-   Archivos generados:

    -   `recording.mp3` → audio final
    -   `transcription.txt` → transcripción del audio completo

---

## ⚡ Notas

-   La transcripción se hace con **Whisper modelo “small”** para la detección de la frase, y puede cambiarse al modelo deseado.
-   El script mantiene compatibilidad con **múltiples dispositivos de audio**.
-   Se recomienda usar **micrófonos con buena sensibilidad** y ambiente silencioso para detección precisa de la frase.

---
