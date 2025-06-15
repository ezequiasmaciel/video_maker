from pathlib import Path
import tempfile
from TTS.api import TTS
import streamlit as st

MODEL_NAME = "tts_models/multilingual/libritts/tacotron2-DDC"
_tts = None  # cache global

def _get_tts():
    global _tts
    if _tts is None:
        st.info("Carregando modelo TTS, isso pode levar alguns segundos...")
        _tts = TTS(MODEL_NAME, progress_bar=False, gpu=False)
    return _tts

def synthesize_speech(text: str, lang: str, speaker_id: int = 0) -> str:
    try:
        tts = _get_tts()
        # Usa speaker se suportado
        if hasattr(tts, "speakers") and tts.speakers:
            if speaker_id >= len(tts.speakers):
                speaker_id = 0
            speaker_name = tts.speakers[speaker_id]
            wav = tts.tts(text=text, speaker=speaker_name, language=lang)
        else:
            wav = tts.tts(text=text, language=lang)

        tmp_path = Path(tempfile.mkstemp(suffix=".wav")[1])
        tts.save_wav(wav, tmp_path)
        return str(tmp_path)

    except Exception as e:
        st.error(f"Erro no TTS: {e}")
        print(f"Erro detalhado no TTS: {e}")
        raise
