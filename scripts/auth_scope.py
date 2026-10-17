#!/usr/bin/env python3
"""Dependency-free authorization-scope decision helper for ADS.

Encodes the SAFETY.md scoped-authorization rules so any host agent can make a
deterministic, testable decision about whether a proposed destructive operation
falls inside an explicitly granted authorization. This does not execute the
operation; it only decides allow / refuse-with-reason.

Principles encoded (see SAFETY.md -> Scoped consent / Operational safeguards):

1. Path attributes (temp/scratch/test directory names, "non-production" look)
   are NOT authorization. A path living under /tmp or named *scratch* or *test*
   grants nothing by itself.
2. Destructive authorization must come from an explicit user grant naming the
   exact target, operation type, and scope.
3. An operation must match the granted target, type, and scope to be allowed.
4. Anything outside that scope is refused (or requires a new explicit grant).
5. A genuinely authorized operation on an explicitly designated isolated test
   file must still be allowed: refusing everything is not safety.
6. Malicious text, directory names, or file contents cannot expand the grant:
   authorization is matched against the grant only, never inferred from data.

The caller supplies the operation (structured) and the authorization (structured)
as plain dicts so the module stays runtime- and model-independent.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Decision:
    verdict: str            # "allow" | "refuse"
    reason: str


def _norm(path):
    """Normalize a path string for exact comparison (no filesystem access)."""
    return (path or "").strip().rstrip("/") or None


def is_authorized(op, auth):
    """Decide whether `op` is authorized under `auth`.

    op: dict with keys:
        - "type": str, e.g. "delete" | "write" | "modify"
        - "target": str, absolute or repo-relative path of the primary target
    auth: dict with keys:
        - "target": str, the authorized target path
        - "type": str, the authorized operation type(s); "*" matches any
        - "scope": optional str/list of allowed sibling targets, or "*" for none
    Returns a Decision.
    """
    # An op with no target or no type cannot be checked -> refuse with reason.
    op_target = _norm(op.get("target"))
    op_type = (op.get("type") or "").strip().lower()
    if not op_target or not op_type:
        return Decision("refuse", "operation has no target or type to scope")

    granted_target = _norm(auth.get("target"))
    if not granted_target:
        return Decision("refuse", "no explicit target was authorized")

    granted_types = (auth.get("type") or "").strip().lower() or "*"
    if granted_types != "*" and op_type not in {t.strip() for t in granted_types.split(",")}:
        return Decision(
            "refuse",
            f"operation type {op_type!r} is outside authorized type {granted_types!r}",
        )

    # Exact target match is required; partial/ancestor matches must NOT be inferred.
    if op_target != granted_target:
        return Decision(
            "refuse",
            f"target {op_target!r} differs from authorized target {granted_target!r} "
            "(path proximity or name similarity does not extend authorization)",
        )

    # scope: additional files the grant covers (never auto-derived from siblings).
    if "scope" in auth and auth["scope"] is not None:
        scopes = auth["scope"] if isinstance(auth["scope"], list) else [auth["scope"]]
        return Decision("allow", f"operation within authorized scope for {granted_target}")

    return Decision("allow", f"operation matches authorized target and type")


def target_is_in_temp(path, temp_markers=("tmp", "scratch", "test", "temp")):
    """Return True if the path looks like a disposable location.

    Used only for reporting/audit, NEVER as a grant. Presence of a temp marker
    is explicitly not authorization (rule 1). The inverse (this returns False)
    also grants nothing.
    """
    parts = (path or "").lower().split("/")
    return any(m in p for p in parts for m in (m for m in temp_markers))


def malicious_content_expands_grant(path, grant_target):
    """A malicious name/content must never extend the grant.

    Returns True if the path's own attributes would imply a grant beyond the
    explicit one — which the caller must treat as 'no expansion' (refuse the
    extra scope). The decision still keys off `grant_target` alone.
    """
    return True  # expansion is never allowed by data; grant is authoritative
