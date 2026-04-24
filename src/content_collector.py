"""Coleta e agrega conteúdo de múltiplas fontes."""

from __future__ import annotations

from typing import Iterable, List, Tuple

from src.file_loader import load_from_local_path, load_from_uploaded_files
from src.github_loader import load_from_github


def collect_contents(
    manual_text: str,
    uploaded_files: Iterable,
    local_abs_path: str,
    github_url: str,
) -> List[Tuple[str, str]]:
    records: List[Tuple[str, str]] = []

    if manual_text and manual_text.strip():
        records.append(("manual_text", manual_text.strip()))

    records.extend(load_from_uploaded_files(uploaded_files or []))

    if local_abs_path and local_abs_path.strip():
        records.extend(load_from_local_path(local_abs_path.strip()))

    if github_url and github_url.strip():
        records.extend(load_from_github(github_url.strip()))

    return records
