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
        # ←‑‑‑ Mostra a mensagem completa no Streamlit
        import streamlit as st
        st.error(f"⚠️ Falha no TTS: {e}")
        raise


    # Salva o áudio temporariamente
    tmp_path = Path(tempfile.mkstemp(suffix=".wav")[1])
    tts.save_wav(wav, tmp_path)
    return str(tmp_path)
