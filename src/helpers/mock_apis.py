from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List


_CREATE_FIXTURE_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "fixtures"
    / "github_issue_creation_fixture.json"
)
_ASSIGN_FIXTURE_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "fixtures"
    / "github_issue_assignment_fixture.json"
)
_SLACK_NOTIFY_FIXTURE_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "fixtures"
    / "slack_notify_fixture.json"
)

with _CREATE_FIXTURE_PATH.open("r", encoding="utf-8") as _f:
    _ISSUE_FIXTURE: Dict[str, Any] = json.load(_f)


CREATED_ISSUES: List[Dict[str, Any]] = []
_issue_number_counter: int = int(_ISSUE_FIXTURE.get("number", 0))

with _ASSIGN_FIXTURE_PATH.open("r", encoding="utf-8") as _af:
    _ASSIGNMENT_FIXTURE: Dict[str, Any] = json.load(_af)
with _SLACK_NOTIFY_FIXTURE_PATH.open("r", encoding="utf-8") as _sf:
    _SLACK_NOTIFY_FIXTURE: Dict[str, Any] = json.load(_sf)


def _next_issue_number() -> int:
    global _issue_number_counter
    _issue_number_counter += 1
    return _issue_number_counter


def create_issue(title: str, description: str, severity: str) -> Dict[str, Any]:
    issue = deepcopy(_ISSUE_FIXTURE)
    number = _next_issue_number()

    issue["id"] = number
    issue["number"] = number
    issue["title"] = str(title)
    issue["body"] = str(description)

    base_repo = "https://api.github.com/repos/octocat/Hello-World"
    issue["url"] = f"{base_repo}/issues/{number}"
    issue["labels_url"] = f"{base_repo}/issues/{number}/labels{{/name}}"
    issue["comments_url"] = f"{base_repo}/issues/{number}/comments"
    issue["events_url"] = f"{base_repo}/issues/{number}/events"
    issue["html_url"] = f"https://github.com/octocat/Hello-World/issues/{number}"

    sev_slug = str(severity).strip().lower()
    label_name = f"severity:{sev_slug}"
    if issue.get("labels"):
        issue["labels"][0]["name"] = label_name
        issue["labels"][0]["url"] = f"{_ISSUE_FIXTURE['repository_url']}/labels/{label_name}"
    else:
        issue["labels"] = [{
            "id": 0,
            "url": f"{_ISSUE_FIXTURE['repository_url']}/labels/{label_name}",
            "name": label_name,
            "color": "f29513",
            "default": True,
            "description": "Indicates the severity of the issue",
        }]

    CREATED_ISSUES.append(issue)
    return issue


def assign_issue(issue_id: int, assignee: str) -> Dict[str, Any]:
    """Mock assign issue API. Returns a GitHub-like issue payload after assignment."""
    assigned_issue: Dict[str, Any] | None = None
    try:
        for it in reversed(CREATED_ISSUES):
            if int(it.get("number", -1)) == int(issue_id):
                it["assignee"] = {"login": str(assignee)}
                # also mirror in assignees array
                it["assignees"] = [{"login": str(assignee)}]
                assigned_issue = it
                break
    except Exception:
        assigned_issue = None

    # Build response from assignment fixture
    resp = deepcopy(_ASSIGNMENT_FIXTURE)
    number = int(issue_id)
    base_repo = resp.get("repository_url", "https://api.github.com/repos/octocat/Hello-World")
    resp["id"] = number
    resp["number"] = number
    resp["url"] = f"{base_repo}/issues/{number}"
    resp["labels_url"] = f"{base_repo}/issues/{number}/labels{{/name}}"
    resp["comments_url"] = f"{base_repo}/issues/{number}/comments"
    resp["events_url"] = f"{base_repo}/issues/{number}/events"
    resp["html_url"] = f"https://github.com/octocat/Hello-World/issues/{number}"

    # Fill in dynamic fields when we have the created issue
    if assigned_issue is not None:
        resp["title"] = assigned_issue.get("title", resp.get("title"))
        resp["body"] = assigned_issue.get("body", resp.get("body"))
        if assigned_issue.get("labels"):
            resp["labels"] = assigned_issue["labels"]
    # assignee info
    assignee_obj = dict(resp.get("assignee") or {})
    assignee_obj["login"] = str(assignee)
    resp["assignee"] = assignee_obj
    resp["assignees"] = [assignee_obj]

    return resp


def notify_slack(channel: str, text: str) -> Dict[str, object]:
    """Mock Slack notify API response based on a Slack-like fixture."""
    resp: Dict[str, Any] = deepcopy(_SLACK_NOTIFY_FIXTURE)
    resp["channel"] = str(channel)
    # update nested message text if present
    if isinstance(resp.get("message"), dict):
        resp["message"]["text"] = str(text)
        # update simple Block Kit section text if present
        blocks = resp["message"].get("blocks")
        if isinstance(blocks, list) and blocks:
            block0 = blocks[0]
            if isinstance(block0, dict) and isinstance(block0.get("text"), dict):
                block0["text"]["text"] = str(text)
    return resp


def reset_mocks() -> None:
    """Reset in-memory mock state for tests: clears issues and resets counter."""
    global _issue_number_counter
    CREATED_ISSUES.clear()
    _issue_number_counter = int(_ISSUE_FIXTURE.get("number", 0))


__all__ = ["create_issue", "assign_issue", "notify_slack", "CREATED_ISSUES", "reset_mocks"]


