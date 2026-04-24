"""Camada de sumarização com fallback local."""

from __future__ import annotations

from src.claude_client import ClaudeClient
from src.config import INTERNAL_SYSTEM_PROMPT


def build_user_prompt(intent_instruction: str, additional_instruction: str, content: str) -> str:
    extra = f"\nInstrução adicional do usuário: {additional_instruction}\n" if additional_instruction else ""
    return (
        f"Intenção principal: {intent_instruction}.\n"
        f"{extra}\n"
        "Conteúdo técnico filtrado:\n"
        f"{content}"
    )


def summarize_content(intent_instruction: str, additional_instruction: str, content: str) -> str:
    prompt = build_user_prompt(intent_instruction, additional_instruction, content)
    client = ClaudeClient()
    return client.summarize(INTERNAL_SYSTEM_PROMPT, prompt)
