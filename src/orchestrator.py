"""Orchestrator skeleton for the Bug Triage Agent.

Implement the orchestration logic inside `orchestrate_from_command`.
Expected final output JSON (deterministic):
{
  "ticket_id": "...",
  "ticket_description": "...",
  "assignee": "...",
  "severity": "Critical|Major|Minor|Trivial"
}
"""

from __future__ import annotations

from typing import Any, Dict

def orchestrate_from_command(command: str) -> Dict[str, Any]:
    """Implement this function: orchestrate parse → classify → create → assign → notify."""
    raise NotImplementedError("orchestrate_from_command must be implemented by the candidate")
