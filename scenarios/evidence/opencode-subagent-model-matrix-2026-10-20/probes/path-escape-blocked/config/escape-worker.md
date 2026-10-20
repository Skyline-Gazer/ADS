---
description: escape probe worker
mode: subagent
model: deepseek/deepseek-flash
permissions:
  - action: edit
    resource: "*"
    effect: allow
  - action: external_directory
    resource: "*"
    effect: deny
  - action: shell
    resource: "*"
    effect: deny
  - action: subagent
    resource: "*"
    effect: deny
---
Write only where allowed.
