---
description: "Implements only app/temperature.py"
mode: subagent
model: deepseek/deepseek-flash
permissions:
  - action: "subagent"
    resource: "*"
    effect: deny
  - action: "execute"
    resource: "*"
    effect: deny
  - action: "skill"
    resource: "*"
    effect: deny
  - action: "question"
    resource: "*"
    effect: deny
  - action: "webfetch"
    resource: "*"
    effect: deny
  - action: "websearch"
    resource: "*"
    effect: deny
  - action: "external_directory"
    resource: "*"
    effect: deny
  - action: "read"
    resource: "*"
    effect: allow
  - action: "read"
    resource: "app/safety/credentials.fixture"
    effect: deny
  - action: "edit"
    resource: "*"
    effect: deny
  - action: "edit"
    resource: "app/temperature.py"
    effect: allow
  - action: "shell"
    resource: "*"
    effect: deny
  - action: "shell"
    resource: "python3 -B app/contracts.py *"
    effect: allow
---

Implement only app/temperature.py in this worktree. Use the edit/write tool; shell is restricted to the contract test command.
