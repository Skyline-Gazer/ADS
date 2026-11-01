---
name: bootstrap
description: Create the smallest runnable project and adopt ADS without mandatory runtime, sandbox or extra governance.
---
# Bootstrap

1. Define the user's goal, stack constraints and actual authorization. Inspect the target project/host for existing code, lockfiles, native Skills, toolchain and CI; reuse before installing anything.
2. Create only the minimal runnable vertical slice, declared build/test commands and tests able to detect the intended behavior. Add CI only if its value is real; do not force Docker, remote infrastructure or a second task system.
3. Use a short project-root [AGENTS.md template](../../templates/AGENTS.md) with purpose, architecture/paths, build/test commands, Git/merge/deploy effects and sensitive operations. Pin the reviewed ADS release as a `.ads` submodule when adopting the standard; don't follow mutable branches.
4. Additional [profiles](../../profiles/README.md) and their scripts are **opt-in**. A missing OS sandbox, security audit, CodeGraph or RTK never prevents ordinary development. Do not misrepresent prompt-only restrictions as effective isolation.
5. Run the smallest relevant functional check and report actual evidence, not assumed PASS.

Keep existing Git provider and remote setup unless the owner separately authorizes a change. See [lite](../../docs/lite-adoption.md) and [provider selection](../../docs/git-provider.md). No multi-stage bootstrap approvals or automatic production changes.
