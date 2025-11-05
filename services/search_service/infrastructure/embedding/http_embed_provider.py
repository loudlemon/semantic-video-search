import httpx
from ...domain.repositories import EmbeddingProvider


class HttpEmbeddingProvider(EmbeddingProvider):
    def __init__(self, base_url: str, client: httpx.AsyncClient):
        self._base_url = base_url.rstrip("/")
        self._client = client

    async def embed_text(self, text: str) -> list[float]:
        url = f"{self._base_url}/embed-text"
        resp = await self._client.post(url, json={"text": text})
        resp.raise_for_status()
        data = resp.json()
        return data["embedding"]
