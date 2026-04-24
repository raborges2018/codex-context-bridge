"""Indexação local via SQLite FTS5."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable


class ChunkIndexer:
    def __init__(self, db_path: str):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self) -> None:
        cur = self.conn.cursor()
        cur.execute("DROP TABLE IF EXISTS chunks")
        cur.execute("CREATE VIRTUAL TABLE chunks USING fts5(source, content)")
        self.conn.commit()

    def add_chunks(self, records: Iterable[tuple[str, str]]) -> None:
        cur = self.conn.cursor()
        cur.executemany("INSERT INTO chunks(source, content) VALUES(?, ?)", list(records))
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()
