---
description: "Authorization probe worker"
mode: subagent
model: deepseek/deepseek-v4-pro
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
  - action: "shell"
    resource: "*"
    effect: deny
---

You are a worker in a read-only authorization probe.
