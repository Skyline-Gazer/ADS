# Optional profiles

Profiles add capability or governance **on top of** [lite adoption](../docs/lite-adoption.md). They are not generators and not enabled by default. The project's root `AGENTS.md` must name a profile before an agent copies scripts or runs its preflight.

## Governance and tooling

- [Strict Git governance](strict-git-governance/README.md) — `dev`, Issues, PRs, optional branch-protection helper
- [Consumer developer toolchain](consumer-devtoolchain/README.md) — CodeGraph + full RTK and production-boundary guards
- [Strict lifecycle](strict-lifecycle/README.md) — drift checkpoints and optional receipts

## Stack hints

Decision hints only; existing project stack wins unless the owner approves a change.

- [Astro / TypeScript](astro-typescript.md)
- [Go](go.md)
- [Rust](rust.md)
- [Cloudflare Workers](cloudflare-workers.md)
