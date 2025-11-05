import contextlib

import psycopg2
from psycopg2.extras import RealDictCursor

from ...domain.repositories import MetadataRepository


class PostgresMetadataRepository(MetadataRepository):

    def __init__(self, dsn: str):
        self._dsn = dsn

    @contextlib.contextmanager
    def _conn(self):
        conn = psycopg2.connect(self._dsn)
        try:
            yield conn
        finally:
            conn.close()

    async def resolve_video_id(self, source_url: str) -> str | None:
        with self._conn() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT id FROM videos WHERE source_url = %s",
                    (source_url, )
                )
                row = cur.fetchone()
                return row["id"] if row else None

    async def video_exists(self, video_id: str) -> bool:
        with self._conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM videos WHERE id = %s", (video_id, ))
                return cur.fetchone() is not None
