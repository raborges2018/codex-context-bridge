"""Busca semântica simples por FTS5 + fallback por LIKE."""

from __future__ import annotations

import sqlite3
from typing import List, Tuple


def search_chunks(db_path: str, query: str, limit: int) -> List[Tuple[str, str]]:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT source, content FROM chunks WHERE chunks MATCH ? LIMIT ?",
            (query, limit),
        )
        rows = cur.fetchall()
        if rows:
            return rows

        cur.execute(
            "SELECT source, content FROM chunks WHERE content LIKE ? LIMIT ?",
            (f"%{query[:50]}%", limit),
        )
        return cur.fetchall()
    finally:
        conn.close()
