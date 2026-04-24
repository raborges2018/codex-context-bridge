"""Cliente de integração com a API da Anthropic."""

from __future__ import annotations

import os

from anthropic import Anthropic

from src.config import DEFAULT_MODEL


class ClaudeClient:
    def __init__(self, model: str = DEFAULT_MODEL):
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY não foi definida no ambiente.")
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def summarize(self, system_prompt: str, user_prompt: str, max_tokens: int = 1800) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        texts = [block.text for block in response.content if getattr(block, "type", "") == "text"]
        return "\n".join(texts).strip()
