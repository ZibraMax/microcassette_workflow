# Microcassette Workflow — Transcripción de audio a texto

Proyecto para digitalizar y transcribir audios procedentes de microcassettes a texto utilizando Python y herramientas de reconocimiento de voz.

## Descripción

Este repositorio contiene utilidades y scripts para:

-   Pasar audios grabados en microcassette a archivos de audio digitales.
-   Preprocesar (limpieza, normalización) esos audios.
-   Transcribir el audio a texto usando modelos de reconocimiento de voz (offline u online según la configuración).

## Características

-   Flujo de trabajo sencillo para preparar y transcribir audios.
-   Soporte para pasos de preprocesado (reducción de ruido, normalización de volumen).
-   Salida en texto plano para integración con otros sistemas.

## Requisitos

-   Python 3.8+
-   Dependencias listadas en `requirements.txt` (instalar con pip).
-   Software opcional: herramientas de edición de audio (por ejemplo, Audacity) para digitalizar cintas si aún no están en formato digital.

## Instalación

1. Crear y activar un entorno virtual (recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Uso

El repositorio incluye el archivo `script.py` como punto de partida. Dependiendo de tu flujo, los pasos típicos son:

1. Obtener archivos de audio digitalizados desde la cinta (WAV/FLAC/MP3).
2. Ejecutar el script de preprocesado (si existe) para normalizar y limpiar el audio.
3. Ejecutar el script de transcripción.

Ejemplo genérico:

```bash
python script.py --input path/to/audio.wav --output transcripcion.txt
```

Nota: `script.py` puede requerir argumentos distintos según la implementación. Revisa su cabecera o ejecuta `python script.py --help`.

## Preparación de audio (consejos)

-   Graba o exporta en WAV o FLAC para mejor calidad.
-   Eliminar silencios largos y reducir ruido mejora la precisión.
-   Mantener una frecuencia de muestreo consistente (por ejemplo, 16 kHz o 44.1 kHz).

## Formato de salida

El resultado por defecto es un archivo de texto plano con la transcripción completa. Se pueden añadir opciones para obtener subtítulos (`.srt`) o JSON con timestamps.

## Contribuir

Si quieres colaborar:

-   Abre un issue describiendo la mejora o bug.
-   Envía un PR con cambios claros y pruebas cuando aplique.

## Licencia

Por defecto, no se especifica una licencia en este repositorio. Añade un archivo `LICENSE` con la licencia deseada (por ejemplo, MIT) si quieres permitir el uso público.

---

Si quieres, puedo:

-   Añadir ejemplos concretos de comandos según las dependencias instaladas.
-   Implementar un CLI básico en `script.py` y documentarlo aquí.
