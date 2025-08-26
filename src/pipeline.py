"""Simple CLI to run the bug triage orchestration from a free-text command."""

from __future__ import annotations

import json
import sys
from typing import Any, Dict

from .orchestrator import orchestrate_from_command


def run(command: str) -> Dict[str, Any]:
    """Run the orchestration on the provided free-text command."""
    return orchestrate_from_command(command)


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        sys.stdout.write(
            json.dumps(
                {"error": {"code": "USAGE", "message": "Provide the free-text command as arguments"}},
                ensure_ascii=False,
                separators=(",", ":"),
            )
        )
        sys.stdout.flush()
        return 1
    command = " ".join(args)
    out = run(command)
    sys.stdout.write(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    sys.stdout.flush()
    return 0


__all__ = ["run", "main"]


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

