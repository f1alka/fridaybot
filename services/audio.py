import subprocess
import os
from faster_whisper import WhisperModel
from loguru import logger
from config import settings

# Инициализация модели (при старте воркера)
model = WhisperModel(settings.whisper_model, device="cpu", compute_type="int8")

def process_audio(ogg_path: str) -> str:
    """Конвертация OGG в WAV и расшифровка."""
    wav_path = ogg_path.replace(".ogg", ".wav")
    
    # 1. FFmpeg: OGG Opus -> WAV 16kHz mono
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", ogg_path, "-ar", "16000", "-ac", "1", wav_path],
            check=True, capture_output=True
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg error: {e.stderr.decode()}")
        raise

    # 2. Faster-Whisper
    segments, info = model.transcribe(wav_path, beam_size=5, language="ru")
    text = " ".join([segment.text for segment in segments])
    
    # Очистка
    os.remove(ogg_path)
    os.remove(wav_path)
    
    logger.info(f"Transcribed: {text[:100]}...")
    return text.strip()