"""Narração multilíngue via Coqui TTS (your_tts)."""
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


def synthesize_speech(text: str, lang: str, speaker_id=None) -> str:
    tts = _get_tts()

    # Fallback seguro para speaker_id
    try:
        if speaker_id is not None:
            wav = tts.tts(text=text, language=lang, speaker=speaker_id)
        else:
            wav = tts.tts(text=text, language=lang)
    except Exception as e:
        # Erro ao usar speaker_id — tentar sem ele
        print(f"[AVISO] Erro com speaker_id={speaker_id}: {e}. Tentando sem speaker...")
        wav = tts.tts(text=text, language=lang)

    # Salva áudio temporário
    tmp_path = Path(tempfile.mkstemp(suffix=".wav")[1])
    tts.save_wav(wav, tmp_path)
    return str(tmp_path)
