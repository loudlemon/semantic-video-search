import os
import tempfile
import ffmpeg
from typing import Iterable, Tuple
from PIL import Image


class FFmpegExtractor:
    def extract(self, video_path: str, fps: int) -> Iterable[Tuple[float, str]]:
        # Use ffmpeg to extract at 1 fps into temp dir; compute timestamps approximately
        out_dir = tempfile.mkdtemp()
        pattern = os.path.join(out_dir, "frame_%06d.jpg")
        (
            ffmpeg
            .input(video_path)
            .filter("fps", fps=fps)
            .output(pattern, qscale=2, vsync="vfr")
            .overwrite_output()
            .run(quiet=True)
        )
        # Approximate timestamps as index / fps
        frames = sorted([f for f in os.listdir(out_dir) if f.endswith(".jpg")])
        for idx, fname in enumerate(frames):
            ts = idx / float(fps)
            yield ts, os.path.join(out_dir, fname)
