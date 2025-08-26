# Problem Statement: AI-Powered Bug Triage Agent (ReWoo)

Your team files and manages bugs daily. Instead of doing everything manually—classifying severity, creating GitHub issues, assigning them, and notifying the team—you’ll build an AI agent that takes a natural language command and runs through the correct workflow automatically.

---

## Task

Build an AI agent that:
- Parses a free-text command (e.g., “Create a bug for login failure, assign to Alice, and notify the team”).
- Uses ReWoo to implement two tools (Command Parser and Severity Classifier).
- Orchestrates mocked GitHub/Slack integrations to return a final deterministic JSON result.

---

## Requirements

- Implement two ReWoo tools:
  1) Command Parser Tool
     - Input: free-text command
     - Output (JSON-only, deterministic):
      ```json
      {
        "actions": ["classify", "create", "assign", "notify"],
        "bug_description": "...",
        "employee_name": "..."
      }
      ```
     - Behavior: Extract actions (subset of classify/create/assign/notify), `bug_description` (required), and `employee_name` (optional/null if absent) and `severity` (optional/null). Implement full ReWoo internally; do not emit prose.

  2) Bug Severity Classifier Tool
     - Input: one-line bug description
     - Output (JSON-only, deterministic):
      ```json
      { "severity": "Critical", "reason": "..." }
      ```
     - The `reason` must be a concise justification referencing the scale (no chain-of-thought, no hidden deliberations).
     - **Severity scale for classification:**
        - Critical: Causes system crash, data loss, or severe security issues.
        - Major: Core functionality broken, but not a full crash.
        - Minor: Cosmetic issues, small glitches, typos.
        - Trivial: Negligible impact, very low priority.
  
- Workflow must run in this order:
  1) Classify (if missing or explicitly requested)
  2) Create ticket (GitHub issue mock)
  3) Assign ticket (if employee given)
  4) Notify (if explicitly requested, or always if severity is Critical)

- Action dependencies (must be enforced):
  - Assign and Notify require Create.
  - Violations → return error JSON.

- Final output (JSON-only, deterministic):
  ```json
  {
    "ticket_id": "...",
    "ticket_description": "...",
    "assignee": "...",
    "severity": "<critical|major|minor|trivial>"
  }
  ```
- All errors must also be JSON-only:
  - Missing description → `{ "error": "Missing bug_description" }`
  - Assign/notify without create → `{ "error": "Invalid command: 'assign' and 'notify' require 'create'" }`
  - Unsupported action → `{ "error": "Unsupported action: <action>" }`
  - Assign with no employee → `{ "error": "Missing employee_name for assign action" }`
---

## Example

Input:
```
"Create a bug for login fails with 500 on submit. Assign to Alice and notify."
```

Parser output:
```json
{
  "actions": ["classify", "create", "assign", "notify"],
  "bug_description": "login fails with 500 on submit",
  "employee_name": "Alice"
}
```

Classifier output:
```json
{ "severity": "major", "reason": "HTTP 500 on login breaks core auth without full crash" }
```

Final workflow output:
```json
{
  "ticket_id": "ISSUE-123",
  "ticket_description": "login fails with 500 on submit",
  "assignee": "Alice",
  "severity": "major"
}
```

If the severity were Critical, the workflow would also call the Slack notify mock before returning the final JSON.

---

## Constraints
- All outputs must be JSON-only, deterministic (no prose).
- Severity is always required (from input or classifier).
- Must use provided helpers:
    - `src/helpers/llm.py` → for ReWoo LLM calls.
    - `src/helpers/mock_apis.py` → for mocked GitHub/Slack APIs.
- Internal reasoning must never leak into outputs (only short reason allowed in classifier).
- Code should be clean, readable, and maintainable.