"""Busca imagens/vídeos gratuitos coerentes usando Pexels/Pixabay."""
import requests
from typing import List
import tempfile
import pathlib
import os

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "COLE_SUA_CHAVE")


def fetch_assets(script: str) -> List[str]:
    tmpdir = pathlib.Path(tempfile.mkdtemp())
    assets = []
    keywords = set()
    for line in script.split("\n"):
        keywords.update(word.lower() for word in line.split() if len(word) > 4)
    for kw in list(keywords)[:10]:
        url = f"https://api.pexels.com/v1/search?query={kw}&per_page=1"
        r = requests.get(url, headers={"Authorization": PEXELS_API_KEY})
        if r.ok and r.json().get("photos"):
            img_url = r.json()["photos"][0]["src"]["large"]
            img_data = requests.get(img_url).content
            path = tmpdir / f"{kw}.jpg"
            path.write_bytes(img_data)
            assets.append(str(path))
    return assets
