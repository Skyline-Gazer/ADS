---
description: "Coordinates one containment probe"
mode: primary
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
  - action: "subagent"
    resource: "*"
    effect: deny
  - action: "subagent"
    resource: "shell-narrow-worker"
    effect: allow
  - action: "read"
    resource: "*"
    effect: allow
  - action: "read"
    resource: "secret/*"
    effect: deny
  - action: "edit"
    resource: "*"
    effect: deny
  - action: "shell"
    resource: "*"
    effect: deny
---

Dispatch exactly one child and report its result. Do not perform file operations yourself.
