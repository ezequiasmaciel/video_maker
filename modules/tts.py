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


def synthesize_speech(text: str, lang: str, speaker_id=0) -> str:
    tts = _get_tts()

    # Garante que speaker_id é inteiro
    speaker_id = int(speaker_id)

    # Lista de vozes disponíveis
    available_speakers = tts.speakers

    # Verificação de índice válido
    if speaker_id >= len(available_speakers):
        raise ValueError(
            f"speaker_id {speaker_id} inválido. Existem apenas {len(available_speakers)} vozes disponíveis."
        )

    # Seleciona nome da voz
    speaker_name = available_speakers[speaker_id]

    # Gera o áudio
    wav = tts.tts(text=text, language=lang, speaker=speaker_name)

    # Salva em arquivo temporário
    tmp_path = Path(tempfile.mkstemp(suffix=".wav")[1])
    tts.save_wav(wav, tmp_path)
    return str(tmp_path)
