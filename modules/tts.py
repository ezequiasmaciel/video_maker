"""Narração multilíngue via Coqui TTS (m_multi)."""
from pathlib import Path
import tempfile
from TTS.api import TTS

# Modelo multilíngue compatível com Coqui TTS
MODEL_NAME = "tts_models/multilingual/multi-dataset/your_tts"
_tts = None  # cache global


def _get_tts():
    global _tts
    if _tts is None:
        _tts = TTS(MODEL_NAME, progress_bar=False, gpu=False)
    return _tts


def synthesize_speech(text: str, lang: str, speaker_id: int = 0) -> str:
    tts = _get_tts()
    wav = tts.tts(text=text, speaker=speaker_id, language=lang)
    tmp_path = Path(tempfile.mkstemp(suffix=".wav")[1])
    tts.save_wav(wav, tmp_path)
    return str(tmp_path)

