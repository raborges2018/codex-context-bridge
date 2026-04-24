"""Resumo offline com detecção automática de tipo de entrada."""

from __future__ import annotations

import re
from collections import Counter
from typing import List

from src.config import PRIORITY_TERMS

ERROR_RE = re.compile(r"\b(error|exception|failed|traceback|fatal|warning|warn)\b", re.IGNORECASE)
PATH_RE = re.compile(r"\b(?:src/|app/|components/|services/|lib/|package\.json|[\w./-]+\.(?:py|ts|tsx|js|jsx|json|md|log|yml|yaml))\b")
DIFF_RE = re.compile(r"\b(diff|commit|pull request|\bpr\b|branch|@@|\+\+\+|---)\b", re.IGNORECASE)
LOG_RE = re.compile(r"\b(INFO|DEBUG|WARN|ERROR|Traceback|Exception|\d{2}:\d{2}:\d{2})\b")
TERMINAL_RE = re.compile(r"^\s*(\$|>|git\s|npm\s|yarn\s|pnpm\s|python\s|pytest\s|ruff\s|flake8\s)", re.IGNORECASE)
QUESTION_HINT_RE = re.compile(r"\b(como|qual|quais|devo|posso|melhor|vale|tem problema|devo|por que|pq)\b", re.IGNORECASE)


def _non_empty_lines(content: str) -> List[str]:
    return [line.strip() for line in content.splitlines() if line.strip()]


def detect_input_type(content: str) -> str:
    lines = _non_empty_lines(content)
    char_count = len(content)

    question_score = 0
    technical_score = 0

    if char_count < 900:
        question_score += 2
    if "?" in content:
        question_score += 2
    if QUESTION_HINT_RE.search(content):
        question_score += 2

    path_hits = len(PATH_RE.findall(content))
    if path_hits > 4:
        technical_score += 2

    if ERROR_RE.search(content):
        technical_score += 3
    if DIFF_RE.search(content):
        technical_score += 3
    if any(TERMINAL_RE.search(line) for line in lines[:100]):
        technical_score += 2

    log_lines = sum(1 for line in lines if LOG_RE.search(line))
    if log_lines > 8:
        technical_score += 2

    # Regras de exclusão para pergunta simples
    if technical_score >= question_score:
        return "technical_context"
    return "question"


def _extract_essential_snippets(content: str, max_lines: int = 10) -> List[str]:
    lines = _non_empty_lines(content)
    scored = Counter()
    for line in lines:
        lower = line.lower()
        scored[line] = sum(1 for term in PRIORITY_TERMS if term in lower)
        if ERROR_RE.search(line):
            scored[line] += 3
        if DIFF_RE.search(line):
            scored[line] += 2
        if PATH_RE.search(line):
            scored[line] += 1
        if TERMINAL_RE.search(line):
            scored[line] += 1
    best = [line for line, _ in scored.most_common(max_lines) if line]
    return best or lines[:max_lines]


def _extract_question(content: str) -> str:
    lines = _non_empty_lines(content)
    question_lines = [line for line in lines if "?" in line]
    if question_lines:
        return question_lines[-1]
    if lines:
        return lines[0]
    return "Não identificado no conteúdo recebido."


def _minimal_context(content: str) -> str:
    lines = _extract_essential_snippets(content, max_lines=4)
    if not lines:
        return "Não identificado no conteúdo recebido."
    return "\n".join(f"- {line}" for line in lines)


def _calc_metrics(original: int, final: int) -> str:
    reduction = 0.0 if original == 0 else ((original - final) / original) * 100
    return (
        f"- Tamanho original: {original} caracteres\n"
        f"- Tamanho final: {final} caracteres\n"
        f"- Redução aproximada: {reduction:.2f}%"
    )


def build_offline_markdown(*, intent: str, additional_instruction: str, selected_text: str, original_size: int) -> str:
    input_type = detect_input_type(selected_text)

    if input_type == "question":
        question = _extract_question(selected_text)
        context_min = _minimal_context(selected_text)
        if additional_instruction.strip():
            question = f"{question} ({additional_instruction.strip()})"

        prompt = f"""--- PROMPT PARA CLAUDE ---

Estou trabalhando no seguinte contexto técnico:

{context_min}

Minha dúvida é:

{question}

Responda de forma objetiva, prática e sem rodeios.
"""
        final_size = len(prompt)
        metrics = _calc_metrics(original_size, final_size)
        return (
            f"{prompt}\n"
            f"--- DADOS DE COMPACTAÇÃO ---\n\n"
            f"- Tipo detectado: pergunta simples\n"
            f"{metrics}"
        )

    snippets = _extract_essential_snippets(selected_text, max_lines=12)
    context_text = "\n".join(f"- {line}" for line in snippets) if snippets else "- Não identificado no conteúdo recebido."
    intent_text = intent if intent.strip() else "Não identificado no conteúdo recebido."
    if additional_instruction.strip():
        intent_text = f"{intent_text} | Instrução adicional: {additional_instruction.strip()}"

    prompt = f"""--- PROMPT PARA CLAUDE ---

Analise o contexto técnico abaixo e me diga exatamente o que fazer.

Contexto:
{context_text}

Minha intenção:
{intent_text}

Responda com:
1. Diagnóstico direto
2. Riscos
3. Próxima ação recomendada
4. Comandos ou ajustes necessários, se houver
"""
    final_size = len(prompt)
    metrics = _calc_metrics(original_size, final_size)
    return (
        f"{prompt}\n"
        f"--- DADOS DE COMPACTAÇÃO ---\n\n"
        f"- Tipo detectado: contexto técnico\n"
        f"{metrics}"
    )
