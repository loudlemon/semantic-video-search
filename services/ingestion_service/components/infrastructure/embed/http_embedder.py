import requests


class HttpEmbedder:

    def __init__(self, base_url: str):
        self._base = base_url.rstrip("/")

    def embed_text(self, text: str) -> list[float]:
        resp = requests.post(f"{self._base}/embed-text", json={"text": text})
        resp.raise_for_status()
        return resp.json()["embedding"]
