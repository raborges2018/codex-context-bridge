"""Geração de chunks com sobreposição."""

from __future__ import annotations

from typing import List


def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]

    chunks: List[str] = []
    start = 0
    step = max(chunk_size - overlap, 1)
    while start < len(text):
        end = start + chunk_size
        piece = text[start:end]
        if piece.strip():
            chunks.append(piece)
        start += step
    return chunks
