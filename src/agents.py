from __future__ import annotations

from typing import Any, Dict

def parse_command_agent(command: str) -> Dict[str, Any]:
    """Implement this function: extract actions, bug_description, and employee_name."""
    raise NotImplementedError("parse_command_agent must be implemented by the candidate")


def classify_agent(description: str) -> Dict[str, str]:
    """Implement this function: return a dict with keys 'severity' and 'reason'."""
    raise NotImplementedError("classify_agent must be implemented by the candidate")


__all__ = ["classify_agent", "parse_command_agent"]
