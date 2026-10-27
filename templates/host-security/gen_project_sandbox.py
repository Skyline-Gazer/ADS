#!/usr/bin/env python3
"""Generate a macOS Seatbelt (sandbox-exec) profile enforcing project-only
read/write for an ADS TUI agent session and ALL its child processes
(MCP servers, indexers, shells, interpreters).

Usage: python3 gen_project_sandbox.py <project_dir> > /tmp/agent.sb
Run:   sandbox-exec -f /tmp/agent.sb <launch agent>
"""
import os, sys

proj = os.path.realpath(sys.argv[1] if len(sys.argv) > 1 else os.getcwd())
home = os.path.realpath(os.path.expanduser("~"))
private = ["/Documents", "/Downloads", "/Music", "/Pictures", "/Movies", "/.ssh", "/Library/Keychains"]

print(f"""(version 1)
(allow default)
;; --- read containment: everything except the project subtree, known private dirs ---
(deny file-read* (require-all (subpath "{home}") (require-not (subpath "{proj}"))))
(deny file-read* (require-all (subpath "/private/tmp") (require-not (subpath "/private/tmp/ads-agent-tmp"))))
(deny file-read* {' '.join(f'(subpath "{home}{p}")' for p in private)})
;; --- write containment: project + a scratch tmp dir only ---
(deny file-write* (require-all (subpath "{home}") (require-not (subpath "{proj}"))))
(deny file-write* (require-all (subpath "/private/tmp") (require-not (subpath "/private/tmp/ads-agent-tmp"))))
""")
