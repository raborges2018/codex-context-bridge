"""Resumo offline por heurísticas, sem uso de APIs externas de IA."""

from __future__ import annotations

import re
from collections import Counter
from typing import Iterable, List

from src.config import PRIORITY_TERMS
from src.intent_router import resolve_next_action

FILE_RE = re.compile(r"(?:[\w./-]+\.(?:py|js|ts|tsx|jsx|md|txt|json|yml|yaml|log|env\.example))")
COMMAND_RE = re.compile(r"^\s*(?:\$|>|npm\s|yarn\s|pnpm\s|python\s|-m\s|git\s|pytest\s|ruff\s|flake8\s|uv\s)", re.IGNORECASE)
ERROR_RE = re.compile(r"\b(error|exception|failed|traceback|fatal|risk|warning|warn)\b", re.IGNORECASE)
DECISION_RE = re.compile(r"\b(decid|escolh|optou|arquitetura|padr[aã]o|estrat[eé]gia|adotad)\b", re.IGNORECASE)
NEXT_RE = re.compile(r"\b(todo|fixme|next|pr[oó]xim|seguir|implementar|ajustar|corrigir)\b", re.IGNORECASE)
STATE_RE = re.compile(r"\b(modified|created|deleted|commit|pr|branch|build|test|lint|merge)\b", re.IGNORECASE)


def _compact_lines(text: str, max_lines: int = 12) -> List[str]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return lines[:max_lines]


def _extract_by_regex(text: str, pattern: re.Pattern[str], cap: int = 15) -> List[str]:
    found: List[str] = []
    for line in text.splitlines():
        if pattern.search(line):
            candidate = line.strip()
            if candidate and candidate not in found:
                found.append(candidate)
        if len(found) >= cap:
            break
    return found


def _extract_commands(text: str, cap: int = 10) -> List[str]:
    out: List[str] = []
    for line in text.splitlines():
        if COMMAND_RE.search(line):
            cmd = line.strip()
            if cmd not in out:
                out.append(cmd)
        if len(out) >= cap:
            break
    return out


def _extract_files(text: str, cap: int = 30) -> List[str]:
    files = FILE_RE.findall(text)
    unique = []
    for file in files:
        if file not in unique:
            unique.append(file)
        if len(unique) >= cap:
            break
    return unique


def _infer_objective(intent: str, lines: List[str]) -> str:
    if not lines:
        return "Não identificado no conteúdo recebido."
    seed = " ".join(lines[:3])
    return f"Com base na intenção '{intent}', o conteúdo indica foco em: {seed[:280]}."


def _infer_state(lines: List[str]) -> List[str]:
    states = [line for line in lines if STATE_RE.search(line)]
    return states[:8]


def _extract_decisions(text: str) -> List[str]:
    return _extract_by_regex(text, DECISION_RE, cap=10)


def _extract_next_steps(text: str) -> List[str]:
    return _extract_by_regex(text, NEXT_RE, cap=8)


def _format_list(items: Iterable[str]) -> str:
    items = [it for it in items if it]
    if not items:
        return "- Não identificado no conteúdo recebido."
    return "\n".join(f"- {item}" for item in items)


def build_offline_markdown(
    *,
    intent: str,
    additional_instruction: str,
    sources: List[str],
    selected_text: str,
    original_size: int,
) -> str:
    lines = _compact_lines(selected_text, max_lines=50)
    objective = _infer_objective(intent, lines)
    state = _infer_state(lines)
    files = _extract_files(selected_text)
    errors = _extract_by_regex(selected_text, ERROR_RE, cap=15)
    commands = _extract_commands(selected_text, cap=10)
    decisions = _extract_decisions(selected_text)
    next_steps = _extract_next_steps(selected_text)

    score_counter = Counter()
    for line in lines:
        lower = line.lower()
        score_counter[line] = sum(1 for term in PRIORITY_TERMS if term in lower)
    essential = [line for line, _ in score_counter.most_common(8) if line]
    if not essential:
        essential = lines[:6]

    next_action = resolve_next_action(intent)
    if additional_instruction.strip():
        next_action = f"{next_action} Considere também: {additional_instruction.strip()}"

    prompt_colar = (
        f"Intenção: {intent}.\n"
        f"Ação solicitada: {next_action}\n"
        "Use o contexto compactado abaixo para executar a próxima etapa com precisão."
    )

    final_markdown = f"""# Contexto Compactado para Claude

## 1. Objetivo
{objective}

## 2. Estado atual do projeto
{_format_list(state)}

## 3. Fontes analisadas
{_format_list(sources)}

## 4. Arquivos relevantes
{_format_list(files)}

## 5. Decisões técnicas identificadas
{_format_list(decisions)}

## 6. Problemas, erros ou riscos
{_format_list(errors)}

## 7. Trechos essenciais preservados
{_format_list(essential)}

## 8. Próxima ação recomendada para o Claude
{next_action}

## 9. Prompt pronto para colar no Claude
```text
{prompt_colar}
```

## 10. Dados de compactação
- tamanho aproximado original: {original_size} chars
- tamanho aproximado final: {{final_size_placeholder}} chars
- redução aproximada: {{reduction_placeholder}}%
"""

    # Acrescenta comandos e próximos passos somente com evidência.
    if commands:
        final_markdown += "\n\n### Comandos identificados\n" + _format_list(commands)
    if next_steps:
        final_markdown += "\n\n### Próximos passos mencionados no conteúdo\n" + _format_list(next_steps)

    final_size = len(final_markdown)
    reduction = 0.0 if original_size == 0 else ((original_size - final_size) / original_size) * 100
    final_markdown = final_markdown.replace("{final_size_placeholder}", str(final_size)).replace(
        "{reduction_placeholder}", f"{reduction:.2f}"
    )
    return final_markdown
