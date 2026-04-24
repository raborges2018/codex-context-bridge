"""Persistência do markdown final."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.config import OUTPUT_DIR


def save_markdown(content: str) -> Path:
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = Path(OUTPUT_DIR) / f"contexto_compactado_{stamp}.md"
    path.write_text(content, encoding="utf-8")
    return path
