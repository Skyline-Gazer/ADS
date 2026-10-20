---
description: "Coordinates the ADS #21 medium task"
mode: primary
model: deepseek/deepseek-flash
permissions:
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
  - action: "subagent"
    resource: "*"
    effect: deny
  - action: "subagent"
    resource: "temp-worker"
    effect: allow
  - action: "subagent"
    resource: "tags-worker"
    effect: allow
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
  - action: "edit"
    resource: "app/tags.py"
    effect: allow
  - action: "shell"
    resource: "*"
    effect: deny
  - action: "shell"
    resource: "python3 -B app/contracts.py *"
    effect: allow
  - action: "shell"
    resource: "git status *"
    effect: allow
  - action: "shell"
    resource: "git diff *"
    effect: allow
  - action: "shell"
    resource: "git log *"
    effect: allow
  - action: "shell"
    resource: "git rev-parse *"
    effect: allow
  - action: "shell"
    resource: "git ls-files *"
    effect: allow
  - action: "shell"
    resource: "ls *"
    effect: allow
  - action: "shell"
    resource: "find *"
    effect: allow
---

Follow the task prompt exactly. Stay inside the configured permissions.
