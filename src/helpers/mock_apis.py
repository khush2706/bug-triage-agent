from __future__ import annotations

from typing import Dict


def create_issue(description: str, severity: str) -> Dict[str, int]:
    """Mock create issue API. Deterministic stub."""
    return {"issue_id": 303}


def assign_issue(issue_id: int, assignee: str) -> Dict[str, object]:
    """Mock assign issue API. Echoes assignment."""
    return {"issue_id": int(issue_id), "assigned_to": str(assignee)}


def notify_slack(channel: str, text: str) -> Dict[str, object]:
    """Mock Slack notify API. Deterministic ack."""
    return {"ok": True, "channel": str(channel)}


__all__ = ["create_issue", "assign_issue", "notify_slack"]


