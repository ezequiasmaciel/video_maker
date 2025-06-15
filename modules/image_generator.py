"""Geração de imagens consistentes por cena via Stable Diffusion."""
from typing import List, Tuple
import tempfile
import pathlib
import re


def split_script_into_scenes(script: str) -> List[str]:
    """Divide pelo marcador CENA N: (insensível a maiúsculas)."""
    scenes = re.split(r"(?i)\n*CENA \d+:?", script)
    return [s.strip() for s in scenes if s.strip()]


def generate_images(script: str) -> Tuple[List[str], List[str]]:
    scenes = split_script_into_scenes(script)
    tmp = pathlib.Path(tempfile.mkdtemp())
    paths = []
    for i, scene in enumerate(scenes):
        path = tmp / f"scene_{i:03}.png"
        # TODO substitua placeholder pela Stable Diffusion real usando diffusers.
        path.write_text(f"FAKE IMAGE – cena {i+1}")
        paths.append(str(path))
    return paths, scenes
