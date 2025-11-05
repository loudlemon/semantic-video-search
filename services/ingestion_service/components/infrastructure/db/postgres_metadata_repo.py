import uuid

import psycopg2


class PostgresMetadata:

    def __init__(self, dsn: str):
        self._dsn = dsn
        self._ensure_schema()

    def _ensure_schema(self):
        conn = psycopg2.connect(self._dsn)
        cur = conn.cursor()
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS videos (
            id UUID PRIMARY KEY,
            source_url TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
        """
        )
        conn.commit()
        cur.close()
        conn.close()

    def create_video(self, source_url: str) -> str:
        vid = str(uuid.uuid4())
        conn = psycopg2.connect(self._dsn)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO videos (id, source_url, status) VALUES (%s, %s, %s)",
            (vid, source_url, "queued")
        )
        conn.commit()
        cur.close()
        conn.close()
        return vid

    def set_status(self, video_id: str, status: str) -> None:
        conn = psycopg2.connect(self._dsn)
        cur = conn.cursor()
        cur.execute(
            "UPDATE videos SET status = %s, updated_at = NOW() WHERE id = %s",
            (status, video_id)
        )
        conn.commit()
        cur.close()
        conn.close()
