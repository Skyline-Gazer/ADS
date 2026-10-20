---
description: escape probe
mode: primary
model: deepseek/deepseek-flash
permissions:
  - action: subagent
    resource: "*"
    effect: deny
  - action: subagent
    resource: escape-worker
    effect: allow
---
Coordinate one worker.
