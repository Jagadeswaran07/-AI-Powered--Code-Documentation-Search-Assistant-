"""Anthropic API client wrapper."""

from __future__ import annotations

import os
from typing import Optional

import anthropic


class AIClient:
    """Thin wrapper around the Anthropic SDK."""

    MODEL = "claude-sonnet-4-6"

    def __init__(self, api_key: Optional[str] = None) -> None:
        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY is not set. "
                "Export it or pass api_key= to AIClient()."
            )
        self._client = anthropic.Anthropic(api_key=key)

    def complete(self, prompt: str, system: str, max_tokens: int = 2048) -> str:
        message = self._client.messages.create(
            model=self.MODEL,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text
