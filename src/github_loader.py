"""Leitura de arquivos e repositórios GitHub públicos."""

from __future__ import annotations

import base64
from pathlib import Path
from typing import List, Tuple
from urllib.parse import urlparse

import requests

from src.config import ALLOWED_EXTENSIONS, IGNORED_DIR_NAMES, PRIORITY_PATH_HINTS

API_BASE = "https://api.github.com"
RAW_HOST = "raw.githubusercontent.com"


def _parse_repo(url: str) -> tuple[str, str]:
    parsed = urlparse(url)
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2:
        raise ValueError("URL de repositório GitHub inválida.")
    return parts[0], parts[1].replace(".git", "")


def _is_file_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc.endswith("github.com") and "/blob/" in parsed.path or parsed.netloc == RAW_HOST


def _to_raw_file_url(url: str) -> str:
    if RAW_HOST in url:
        return url
    return url.replace("https://github.com/", "https://raw.githubusercontent.com/").replace("/blob/", "/")


def load_github_file(url: str) -> List[Tuple[str, str]]:
    raw_url = _to_raw_file_url(url)
    response = requests.get(raw_url, timeout=25)
    response.raise_for_status()
    return [(url, response.text)]


def _priority_score(path: str) -> int:
    score = 0
    for idx, hint in enumerate(PRIORITY_PATH_HINTS):
        if hint in path:
            score += (len(PRIORITY_PATH_HINTS) - idx) * 10
    return score


def _is_relevant_path(path: str) -> bool:
    p = Path(path)
    if any(part in IGNORED_DIR_NAMES for part in p.parts):
        return False
    return p.suffix.lower() in ALLOWED_EXTENSIONS or p.name == ".env.example"


def load_github_repo(url: str) -> List[Tuple[str, str]]:
    owner, repo = _parse_repo(url)
    tree_url = f"{API_BASE}/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    response = requests.get(tree_url, timeout=30)
    response.raise_for_status()
    data = response.json()

    blob_paths = [
        node["path"]
        for node in data.get("tree", [])
        if node.get("type") == "blob" and _is_relevant_path(node.get("path", ""))
    ]
    blob_paths.sort(key=lambda p: _priority_score(p), reverse=True)

    items: List[Tuple[str, str]] = []
    max_files = 200
    for rel_path in blob_paths[:max_files]:
        content_url = f"{API_BASE}/repos/{owner}/{repo}/contents/{rel_path}"
        r = requests.get(content_url, timeout=20)
        if r.status_code != 200:
            continue
        payload = r.json()
        if payload.get("encoding") == "base64":
            raw = base64.b64decode(payload.get("content", "")).decode("utf-8", errors="ignore")
        else:
            raw = payload.get("content", "")
        if raw.strip():
            items.append((f"{url}::{rel_path}", raw))
    return items


def load_from_github(url: str) -> List[Tuple[str, str]]:
    if not url:
        return []
    if _is_file_url(url):
        return load_github_file(url)
    return load_github_repo(url)
