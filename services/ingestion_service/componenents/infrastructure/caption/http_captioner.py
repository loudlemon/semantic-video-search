import requests


class HttpCaptioner:
    def __init__(self, base_url: str):
        self._base = base_url.rstrip("/")

    def caption(self, image_path: str) -> str:
        with open(image_path, "rb") as f:
            resp = requests.post(f"{self._base}/caption", files={"image": ("frame.jpg", f, "image/jpeg")})
        resp.raise_for_status()
        return resp.json()["caption"]
