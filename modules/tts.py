"""Módulo TTS para síntese de fala simples via Coqui TTS."""

from pathlib import Path
import tempfile
from TTS.api import TTS
from TTS.utils.manage import ModelManager

MODEL_NAME = "tts_models/en/ljspeech/tacotron2-DDC"
_tts = None  # cache global


def _get_tts():
    global _tts
    if _tts is None:
        _tts = TTS(MODEL_NAME, progress_bar=False, gpu=False)
    return _tts


def synthesize_speech(text: str) -> str:
    """
    Sintetiza áudio a partir de texto.
    Retorna o caminho do arquivo .wav gerado.
    """
    tts = _get_tts()
    wav = tts.tts(text)
    tmp_path = Path(tempfile.mkstemp(suffix=".wav")[1])
    tts.save_wav(wav, tmp_path)
    return str(tmp_path)


def list_available_models():
    """
    Retorna uma lista dos modelos TTS disponíveis no ambiente.
    """
    manager = ModelManager()
    modelos = []
    for model_type, langs in manager.models_dict.items():
        for lang, datasets in langs.items():
            for dataset, models in datasets.items():
                for model_name in models.keys():
                    modelos.append(f"{model_type}/{lang}/{dataset}/{model_name}")
    return modelos
