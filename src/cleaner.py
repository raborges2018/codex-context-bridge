"""Limpeza de ruído textual antes de indexar/enviar."""

from __future__ import annotations

import re
from collections import Counter

PROGRESS_RE = re.compile(r"^\s*\d+%\|.*$", re.MULTILINE)
DOWNLOAD_RE = re.compile(r"^\s*(Downloading|Fetched|Resolving|Installing)\b.*$", re.IGNORECASE)
WARNING_RE = re.compile(r"\bwarning\b", re.IGNORECASE)
STACK_LINE_RE = re.compile(r"\s+at\s+.*\(.*\)")


def _dedupe_lines(lines: list[str]) -> list[str]:
    counts = Counter(lines)
    kept = []
    seen = Counter()
    for line in lines:
        seen[line] += 1
        if counts[line] > 6 and seen[line] > 3:
            continue
        kept.append(line)
    return kept


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = PROGRESS_RE.sub("", text)
    cleaned_lines = []
    warning_seen = set()
    stack_seen = set()

    for line in text.splitlines():
        if DOWNLOAD_RE.match(line):
            continue

        if WARNING_RE.search(line):
            key = line.strip()
            if key in warning_seen:
                continue
            warning_seen.add(key)

        if STACK_LINE_RE.search(line):
            key = line.strip()
            if key in stack_seen:
                continue
            stack_seen.add(key)

        cleaned_lines.append(line.rstrip())

    cleaned_lines = _dedupe_lines(cleaned_lines)
    normalized = "\n".join(cleaned_lines)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.strip()
