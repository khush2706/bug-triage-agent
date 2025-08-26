from __future__ import annotations

import os
from typing import Any, Optional

from dotenv import load_dotenv  # type: ignore
from langchain_openai import ChatOpenAI  # type: ignore


def _try_load_env() -> None:
    here = os.path.dirname(__file__)
    try:
        load_dotenv(os.path.join(here, "..", ".env.local"))
    except Exception:
        pass


_try_load_env()


def _build_llm(api_key: str, base_url: Optional[str], model: str) -> ChatOpenAI:
    return ChatOpenAI(
        api_key=api_key,
        base_url=base_url,
        model=model,
        temperature=0,
        max_retries=2,
    )


def get_llm() -> Any:
    """Return the shared LLM client instance for ReWoo steps."""
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for LLM usage")
    return _build_llm(api_key=api_key, base_url=api_base, model=model)


__all__ = ["get_llm"]
