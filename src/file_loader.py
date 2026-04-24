"""Carregamento de conteúdo local a partir de uploads e caminhos absolutos."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Tuple

from src.config import ALLOWED_EXTENSIONS, IGNORED_DIR_NAMES


def _is_relevant_file(path: Path) -> bool:
    suffix = path.suffix.lower()
    return path.is_file() and (suffix in ALLOWED_EXTENSIONS or path.name == ".env.example")


def _is_ignored(path: Path) -> bool:
    return any(part in IGNORED_DIR_NAMES for part in path.parts)


def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def load_from_local_path(abs_path: str) -> List[Tuple[str, str]]:
    """Retorna lista (fonte, conteúdo) a partir de arquivo/pasta local."""
    if not abs_path:
        return []

    target = Path(abs_path).expanduser()
    if not target.is_absolute() or not target.exists():
        raise ValueError("Caminho local inválido ou inexistente.")

    items: List[Tuple[str, str]] = []
    if target.is_file():
        if _is_relevant_file(target):
            content = read_file(target)
            if content.strip():
                items.append((str(target), content))
        return items

    for file_path in sorted(target.rglob("*")):
        if _is_ignored(file_path):
            continue
        if not _is_relevant_file(file_path):
            continue
        content = read_file(file_path)
        if content.strip():
            items.append((str(file_path), content))
    return items


def load_from_uploaded_files(files: Iterable) -> List[Tuple[str, str]]:
    items: List[Tuple[str, str]] = []
    for uploaded in files:
        filename = uploaded.name
        suffix = Path(filename).suffix.lower()
        if suffix not in ALLOWED_EXTENSIONS:
            continue
        content = uploaded.getvalue().decode("utf-8", errors="ignore")
        if content.strip():
            items.append((f"upload:{filename}", content))
    return items
