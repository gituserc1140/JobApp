from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free")


def generate_text(
    prompt: str,
    system_prompt: str = "You are a concise career assistant.",
    temperature: float = 0.2,
    max_tokens: int = 700,
) -> Optional[str]:
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        return None

    client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)
    completion = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )

    if not completion.choices:
        return None
    return (completion.choices[0].message.content or "").strip() or None
