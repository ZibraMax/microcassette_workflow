
import os
import ffmpeg
import whisper
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from pathlib import Path
import time
import sys
import tempfile
import unicodedata
import threading
STOP_PHRASES = [
    "fin del dia",       # principal
    "finalizar grabacion",
    "stop recording",    # en inglés, útil si alguien lo dice
    "end of day",
    "grabar terminado",
    "listo el pollo",
    "ok termina",
    "detener grabacion"
]
BLOCK_DURATION = 5
TIME_FORMAT = "%Y%m%d_%H%M%S"
FOLDER = "Transcripcion_" + time.strftime(TIME_FORMAT)

try:
    Path(FOLDER).mkdir(parents=True, exist_ok=True)
except Exception as e:
    print(f"Error creating directory {FOLDER}: {e}")

CHANNELS = 1
AUDIO_FILE = "recording.mp3"
OUTPUT_TXT = "transcription.txt"

BAR_LENGTH = 20


def play_beep(frequency=1000, duration=0.3, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    sd.play(tone, samplerate=sample_rate)
    sd.wait()  # Espera a que termine


def strip_accents(text):
    normalized_text = unicodedata.normalize('NFD', text)
    stripped_text = "".join(
        c for c in normalized_text if not unicodedata.combining(c))
    # Ensure correct re-encoding if needed
    return stripped_text.encode('utf-8').decode('utf-8')


def volume_meter(audio_chunk):
    rms = np.sqrt(np.mean(audio_chunk ** 2))
    level = min(int(rms * BAR_LENGTH * 5), BAR_LENGTH)
    bar = "█" * level + "░" * (BAR_LENGTH - level)
    sys.stdout.write(f"\rNivel: {bar}")
    sys.stdout.flush()


def wav_to_mp3(wav_path, mp3_path):
    (
        ffmpeg
        .input(wav_path)
        .output(mp3_path, audio_bitrate="192k")
        .overwrite_output()
        .run(quiet=True)
    )

    os.remove(wav_path)
    print(f"🎧 MP3 creado: {mp3_path}")


def record_until_phrase(filename):
    print("Presiona ENTER para empezar a grabar...")
    input()
    print("🎙️ Grabando... Presiona ENTER para detener.")

    recorded_audio = []
    block_buffer = []
    stop_flag = {"stop": False}

    def wait_for_enter():
        input()
        print("\n🛑 Deteniendo grabación por usuario. Terminando el bloque actual...")
        stop_flag["stop"] = True

    model = whisper.load_model("small")
    threading.Thread(target=wait_for_enter, daemon=True).start()

    def callback(indata, frames_count, time_info, status):
        if status:
            print(status)
        volume_meter(indata)
        recorded_audio.append(indata.copy())
        block_buffer.append(indata.copy())

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        callback=callback
    )
    full_text = ""
    with stream:
        while not stop_flag["stop"]:
            sd.sleep(int(BLOCK_DURATION * 1000))
            if not block_buffer:
                continue

            block_audio = np.concatenate(block_buffer, axis=0)
            block_buffer.clear()

            # Guardar bloque temporal
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp_wav = tmp.name

            audio_norm = block_audio / max(np.max(np.abs(block_audio)), 1e-6)
            audio_int16 = np.int16(audio_norm * 32767)
            write(tmp_wav, SAMPLE_RATE, audio_int16)

            # Transcribir solo el bloque
            result = model.transcribe(tmp_wav, language="es", fp16=False)
            os.remove(tmp_wav)
            text = result["text"].lower()
            print(f"\nBloque detectado: {text.strip()}")
            full_text += " " + text
            for stop_phrase in STOP_PHRASES:
                if stop_phrase in strip_accents(full_text):
                    print("🛑 Frase detectada:", stop_phrase)
                    stop_flag["stop"] = True
                    play_beep()
                    break
    play_beep(duration=3)
    print("\n⏹️ Grabación finalizada.")

    # Guardar audio completo
    full_audio = np.concatenate(recorded_audio, axis=0)
    full_audio = full_audio / max(np.max(np.abs(full_audio)), 1e-6)
    full_audio = np.int16(full_audio * 32767)
    temp_wav = "temp_recording.wav"
    write(temp_wav, SAMPLE_RATE, full_audio)
    wav_to_mp3(temp_wav, filename)
    print(f"✅ Audio guardado en {filename}")


def record_until_enter(filename):
    print("Presiona ENTER para empezar a grabar...")
    input()

    print("🎙️ Grabando... Presiona ENTER para detener.")
    frames = []

    def callback(indata, frames_count, time, status):
        if status:
            print(status)
        frames.append(indata.copy())
        volume_meter(indata)

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        callback=callback
    )

    with stream:
        input()  # espera ENTER para detener
    TEMP_FILENAME = 'temp_recording.wav'
    audio = np.concatenate(frames, axis=0)
    audio = np.int16(audio / np.max(np.abs(audio)) * 32767)
    write(TEMP_FILENAME, SAMPLE_RATE, audio)
    wav_to_mp3(TEMP_FILENAME, filename)
    print(f"✅ Audio guardado en {filename}")


def transcribe_audio(audio_path, output_txt="transcription.txt", model_size="base", language="es"):
    audio_path = Path(audio_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    print("Loading Whisper model...")
    model = whisper.load_model(model_size)
    print("Transcribing audio...")
    result = model.transcribe(str(audio_path), language=language, fp16=False)
    text = result["text"]
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Transcription saved to: {output_txt}")
    return text


if __name__ == "__main__":
    KEYNAME = "BEHRINGER"
    lista = sd.query_devices()
    DEVICE_ID = None
    possible_idexes = []
    names = {}
    for i, device in enumerate(lista):
        if KEYNAME in device['name'].upper():
            if device['max_input_channels'] > 0:
                print(
                    f"Found device: {device['name']} (ID: {device['index']})")
                SAMPLE_RATE = int(device['default_samplerate'])
                DEVICE_ID = device['index']
                possible_idexes.append(DEVICE_ID)
                names[DEVICE_ID] = device['name']
    if DEVICE_ID is None:
        print(
            f"Usando dispositivo por defecto {sd.default.device[0]} {lista[sd.default.device[0]]['name']}")
        DEVICE_ID = sd.default.device[0]
        SAMPLE_RATE = 44100  # Valor por defecto común
    if len(possible_idexes) > 1:
        print(
            f"Se encontraron multiples dispositivos que coinciden con '{KEYNAME}': {possible_idexes}")
        for idx in possible_idexes:
            try:

                sd.default.device = (idx, None)
                print(
                    f"\nUsando dispositivo ID {idx} {names[idx]} con sample rate {SAMPLE_RATE}\n")
                record_until_phrase(f"{FOLDER}/{AUDIO_FILE}")
                transcribe_audio(f"{FOLDER}/{AUDIO_FILE}",
                                 output_txt=f"{FOLDER}/{OUTPUT_TXT}")
                break
            except Exception as e:
                print(f"Dispositivo ID {idx} fallo con error: {e}")
