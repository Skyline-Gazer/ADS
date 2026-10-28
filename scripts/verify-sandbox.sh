#!/usr/bin/env bash
# ADS #72 automated sandbox regression suite.
# Usage: scripts/verify-sandbox.sh <project-dir> [profile-path]
# Runs positive and synthetic-negative filesystem probes under the hardened
# Seatbelt profile. Never reads real private data; canaries are disposable.
set -u
PROJECT="$(cd "${1:?project dir required}" && pwd)"
PROFILE="${2:-$HOME/.omp/sandbox/$(basename "$PROJECT").sb}"
SCRATCH=/private/tmp/ads-agent-tmp
PASS=0; FAIL=0
EV="${EVIDENCE_OUT:-/private/tmp/ads-agent-tmp/.sandbox-evidence.jsonl}"; : > "$EV"

ok()   { printf '  \033[32mALLOWED\033[0m %s\n' "$1"; PASS=$((PASS+1)); printf '{"name":"%s","expected":"ALLOWED","observed":"ALLOWED"}\n' "$1" >> "$EV"; }
den()  { printf '  \033[31mDENIED \033[0m %s\n' "$1"; PASS=$((PASS+1)); printf '{"name":"%s","expected":"DENIED","observed":"DENIED"}\n' "$1" >> "$EV"; }
bad()  { printf '  \033[31mFAIL   \033[0m %s (rc=%s want %s)\n' "$1" "$2" "$3"; FAIL=$((FAIL+1)); printf '{"name":"%s","expected":"%s","observed":"MISMATCH"}\n' "$1" "$3" >> "$EV"; }

s() { sandbox-exec -f "$PROFILE" "$@"; }

check_allow() { local d="$1"; shift; s "$@" >/dev/null 2>&1 && ok "$d" || bad "$d" "$?" 0; }
check_deny()  { local d="$1"; shift; s "$@" >/dev/null 2>&1 && bad "$d" 0 1 || den "$d"; }

CAN_IN="$PROJECT/.sandbox-canary-inside.txt"
CAN_OUT="/tmp/ads-sandbox-canary-outside.txt"
mkdir -p "$SCRATCH"
echo INSIDE_OK > "$CAN_IN"; echo OUTSIDE_SECRET > "$CAN_OUT"
OUT_LIST=$(dirname "$CAN_OUT")
CAN_OUT_DIR="$OUT_LIST"
echo OUTSIDE_SECRET > "$CAN_OUT"

echo "== positive (must be allowed) =="
check_allow "project file read"          /bin/cat "$CAN_IN"
check_allow "project file write"         /usr/bin/touch "$PROJECT/.sandbox-canary-w.txt"
check_allow "git status"                 git -C "$PROJECT" status --porcelain
check_allow "python project read"        /usr/bin/python3 -c "open('$CAN_IN').read()"
check_allow "node project read"          /usr/bin/env node -e "require('fs').readFileSync('$CAN_IN')"
check_allow "omp state write"            /usr/bin/touch "$HOME/.omp/agent/.sandbox-probe"
check_allow "scratch tmp write"          /usr/bin/touch "$SCRATCH/.sandbox-probe"
command -v rtk >/dev/null && check_allow "rtk project read" rtk cat "$PROJECT/AGENTS.md" || true

echo "== negative (must be denied) =="
check_deny  "outside file read"          /bin/cat "$CAN_OUT"
check_deny  "outside dir list"           /bin/ls "$OUT_LIST"
check_deny  "outside file write"         /usr/bin/touch "$CAN_OUT.w"
check_deny  "python outside read"        /usr/bin/python3 -c "open('$CAN_OUT').read()"
check_deny  "node outside read"          /usr/bin/env node -e "require('fs').readFileSync('$CAN_OUT')"
ln -sf "$CAN_OUT" "$PROJECT/.sandbox-escape-link" 2>/dev/null || true
check_deny  "symlink escape"             /bin/cat "$PROJECT/.sandbox-escape-link"
check_deny  "realpath escape"            /usr/bin/python3 -c "import os;open(os.path.realpath('$CAN_OUT')).read()"
check_deny  "home list"                  /bin/ls "$HOME"
check_deny  "home dotfile read"          /bin/cat "$HOME/.zshrc"
for d in Documents Downloads Music Pictures Movies .ssh; do
  check_deny  "private dir list: ~/$d"   /bin/ls "$HOME/$d"
done
check_deny  "keychains list"             /bin/ls "$HOME/Library/Keychains"
check_deny  "sibling private dir list"   /bin/ls "$HOME/Desktop/Oneplus" 2>/dev/null || den "sibling private dir list (absent)"
check_deny  "other project read"         /bin/cat "$HOME/Desktop/Projects/airingcal-v3/package.json"
check_deny  "/Volumes list"              /bin/ls /Volumes
check_deny  "/Volumes write"             /usr/bin/touch /Volumes/.ads-probe
check_deny  "/var/tmp write"             /usr/bin/touch /var/tmp/.ads-probe
check_deny  "/private write"             /usr/bin/touch /private/.ads-probe
check_deny  "/var/log list"              /bin/ls /var/log
check_deny  "/var/folders list"          /bin/ls /var/folders
check_deny  "/Users list"                /bin/ls /Users
command -v rtk >/dev/null && check_deny "rtk outside read" rtk cat "$CAN_OUT" || true

echo "export function sandboxProbe(){return 1}" > "$PROJECT/.sandbox-cg-probe.ts"
CGTMP="$SCRATCH/.sandbox-cg-$$"; mkdir -p "$CGTMP"
cp "$PROJECT/.sandbox-cg-probe.ts" "$CGTMP/probe.ts"
s node "$HOME/.local/bin/codegraph" init "$CGTMP" >/dev/null 2>&1 && ok "codegraph init (scratch project)" || bad "codegraph init" "$?" 0
s node "$HOME/.local/bin/codegraph" status "$CGTMP" >/dev/null 2>&1 && ok "codegraph status" || bad "codegraph status" "$?" 0
cd "$CGTMP" && s node "$HOME/.local/bin/codegraph" query sandboxProbe >/dev/null 2>&1 && ok "codegraph query" || bad "codegraph query" "$?" 0; cd "$PROJECT"
s node "$HOME/.local/bin/codegraph" index "$CAN_OUT_DIR" >/dev/null 2>&1 && bad "codegraph outside index" 0 1 || den "codegraph outside index"
rm -rf "$CGTMP" "$PROJECT/.sandbox-cg-probe.ts"
OMP_OUT="$(s /opt/homebrew/bin/omp "Reply SANDBOX_PROBE_OK" 2>/dev/null | tail -1)"
case "$OMP_OUT" in *SANDBOX_PROBE_OK*) ok "omp agent one-shot run";; *) bad "omp agent one-shot run" 1 0;; esac

rm -f "$CAN_IN" "$PROJECT/.sandbox-canary-w.txt" "$PROJECT/.sandbox-escape-link" "$HOME/.omp/agent/.sandbox-probe" "$SCRATCH/.sandbox-probe" "$CAN_OUT"
printf '{\"summary\":\"%d passed %d failed\",\"profile\":\"%s\",\"profile_sha256\":\"%s\"}\n' "$PASS" "$FAIL" "$PROFILE" "$(shasum -a 256 "$PROFILE" | cut -d' ' -f1)" >> "$EV"
EVIDENCE_OUT="$EV"
printf '\n%d passed, %d failed\nEvidence: %s\n' "$PASS" "$FAIL" "$EV"
[ "$FAIL" -eq 0 ]
