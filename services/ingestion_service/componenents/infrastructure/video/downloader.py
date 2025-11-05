import tempfile
import os
from pytube import YouTube
import requests
from urllib.parse import urlparse


class SimpleDownloader:
    def download(self, url: str) -> str:
        if "youtube.com" in url or "youtu.be" in url:
            yt = YouTube(url)
            stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
            out_dir = tempfile.mkdtemp()
            path = stream.download(output_path=out_dir, filename="video.mp4")
            return path

        # naive HTTP download for direct links (e.g., S3, Google Drive with direct link)
        out_dir = tempfile.mkdtemp()
        out_path = os.path.join(out_dir, "video.mp4")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(out_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return out_path
