"""Narração multilíngue via Coqui TTS (your_tts ou outro compatível)."""
from pathlib import Path
import tempfile
from TTS.api import TTS

# Modelo compatível com Coqui TTS
MODEL_NAME = "tts_models/multilingual/multi-dataset/your_tts"
_tts = None  # cache global


def _get_tts():
    global _tts
    if _tts is None:
        _tts = TTS(MODEL_NAME, progress_bar=False, gpu=False)
    return _tts


def synthesize_speech(text: str, lang: str, speaker_id: int = 0) -> str:
    tts = _get_tts()

    # Pega lista de locutores (se houver)
    available_speakers = tts.speakers if hasattr(tts, "speakers") and tts.speakers else []

    # Seleciona locutor, se possível
    if available_speakers:
        if speaker_id >= len(available_speakers):
            speaker_id = 0  # fallback
        speaker_name = available_speakers[speaker_id]
    else:
        speaker_name = None

    # Gera áudio com os parâmetros suportados
    try:
        if speaker_name and lang:
            wav = tts.tts(text=text, speaker=speaker_name, language=lang)
        elif speaker_name:
            wav = tts.tts(text=text, speaker=speaker_name)
        elif lang:
            wav = tts.tts(text=text, language=lang)
        else:
            wav = tts.tts(text=text)
    except Exception as e:
        raise ValueError(f"Erro ao gerar áudio com TTS: {e}")

    # Salva o áudio temporariamente
    tmp_path = Path(tempfile.mkstemp(suffix=".wav")[1])
    tts.save_wav(wav, tmp_path)
    return str(tmp_path)
