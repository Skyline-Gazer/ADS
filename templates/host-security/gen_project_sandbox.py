#!/usr/bin/env python3
"""Generate a hardened macOS Seatbelt (sandbox-exec) profile enforcing
deny-default project-only read/write for an ADS TUI agent session and ALL its
child processes (MCP servers, indexers, shells, interpreters).

Usage: python3 gen_project_sandbox.py <project_dir> > <profile>.sb
Run:   sandbox-exec -f <profile>.sb <launch agent>

Model (macOS 27.x validated):
- Non-filesystem operations (process, mach, network) remain allowed; network
  isolation is a separate audit dimension and is NOT provided here.
- Filesystem is deny-default: (deny file-read-data) + (deny file-read-metadata)
  + (deny file-write*) with explicit minimal allows.
- (allow file-read-metadata (subpath "/")) grants path RESOLUTION only —
  lstat/stat of directory entries — never listing or content. Node-based tools
  (CodeGraph) require lstat on path ancestors; this is the minimal primitive
  that satisfies them without leaking directory listings or file contents.
- dyld requires file-read-data on the "/" literal itself; keep it.
- Rule order matters: explicit allows must come AFTER the blanket denies.

Run scripts/verify-sandbox.sh <project> [profile] to validate a generated
profile before use (39 checks, all synthetic canaries).
"""
import os, sys

proj = os.path.realpath(sys.argv[1] if len(sys.argv) > 1 else os.getcwd())
home = os.path.realpath(os.path.expanduser("~"))
private = ["/Documents", "/Downloads", "/Music", "/Pictures", "/Movies", "/.ssh", "/Library/Keychains"]
private += [os.path.realpath(a) for a in sys.argv[2:] if a.startswith("/")]  # extra audited private dirs
tool_roots = ["/.omp", "/.local", "/.cache", "/.npm", "/.bun", "/.cargo", "/go",
              "/.config", "/Library/Application Support/rea"]

print(f"""(version 1)
;; ADS #72 hardened profile — deny-default filesystem, minimal explicit allows.
;; Project: {proj}
;; Non-filesystem ops (process/mach/network) allowed; network NOT filtered here.

(allow default)

;; ---- filesystem deny-default ----
(deny file-read-data)
(deny file-read-metadata)
(deny file-write*)

;; ---- path resolution metadata everywhere (no listing, no content) ----
(allow file-read-metadata (subpath "/"))

;; ---- system runtime: data read-only ----
(allow file-read-data (literal "/") (subpath "/usr") (subpath "/bin") (subpath "/sbin") (subpath "/private") (subpath "/opt") (subpath "/Library") (subpath "/System") (subpath "/dev"))

;; ---- private user data: explicit deny (defense in depth) ----
(deny file-read-data {' '.join(f'(subpath "{home}{p}")' for p in private)})
(deny file-write* {' '.join(f'(subpath "{home}{p}")' for p in private)} (subpath "/Volumes"))

;; ---- project real path: read + write ----
(allow file-read-data (subpath "{proj}"))
(allow file-write* (subpath "{proj}"))

;; ---- audited home toolchain/state roots: read-only ----
(allow file-read-data {' '.join(f'(subpath "{home}{p}")' for p in tool_roots)} (literal "{home}/.gitconfig"))

;; ---- omp state: write only state dirs ----
(allow file-write* {' '.join(f'(subpath "{home}/.omp/{p}")' for p in ("agent", "cache", "run", "logs", "extensions"))})

;; ---- deny system log/temp subtrees before scratch grant ----
(deny file-read-data (subpath "/private/var/log") (subpath "/var/log") (subpath "/private/var/folders") (subpath "/var/folders"))
(deny file-read-data (subpath "/private/tmp") (subpath "/tmp"))
(deny file-write* (subpath "/private/tmp") (subpath "/tmp"))
(allow file-write* (subpath "/dev/null"))
(allow file-read-data (subpath "/dev/null"))

;; ---- isolated scratch ----
(allow file-read-data (subpath "/private/tmp/ads-agent-tmp"))
(allow file-write* (subpath "/private/tmp/ads-agent-tmp"))
""")