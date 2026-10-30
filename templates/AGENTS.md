# Project Agent Instructions

## ADS (lite default)

Source: https://github.com/Skyline-Gazer/ADS  
Local rules: `.ads/` Git submodule (use another path only if already occupied).  
Read at this pin: `.ads/STANDARD.md`, `.ads/SAFETY.md`, `.ads/QUALITY.md`.  
Adoption model: `.ads/docs/lite-adoption.md` (default). Submodule updates: `.ads/docs/how-to-update.md` — advance the gitlink in a dedicated PR when the owner approves; do not track a moving ADS branch.

If `.ads` is inaccessible, report the blocker; do not invent policy text.

## Project facts

Purpose: <one sentence>  
Architecture and key paths: <paths and constraints>  
Build / test: <actual commands>  
Delivery: <default branch; does merge deploy?>  
Sensitive operations: <what needs explicit owner approval>

## Working agreement

Implement minimum sufficient changes for the current goal. Verify with the project's existing tests and CI when relevant. Prefer reusing installed runtimes and declared scripts before adding tooling. Ask once for a concrete missing permission; continue independent safe work inside scope. No extra task database, session journal, or per-phase approval ritual.

Optional ADS profiles (enable only when listed here):

- Strict Git (`dev` + Issue + PR): `.ads/profiles/strict-git-governance/README.md`
- CodeGraph + RTK toolchain: `.ads/profiles/consumer-devtoolchain/README.md`
- Strict lifecycle / drift receipts: `.ads/profiles/strict-lifecycle/README.md`

Stack hints: `.ads/profiles/` (load only what applies).
