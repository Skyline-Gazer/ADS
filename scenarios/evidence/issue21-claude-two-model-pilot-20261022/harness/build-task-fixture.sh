#!/usr/bin/env bash
# Build the immutable medium-complexity task fixture for the ADS #21 two-model pilot.
#
# Requirements from v0.3-subagent-model-matrix.md:
#   - one MEDIUM task of two genuinely separate modules
#   - a common test/build oracle both cells must satisfy
#   - the same starting Git fixture, expected behavior, test oracle and task text
#   - numeric and malformed-input edge cases BEFORE measuring
#   - no reuse of historical failed timing as a correctness-matched baseline
#
# Two independent modules with a shared harness:
#   mod-a  text normalisation + token statistics  (pure functions, no I/O)
#   mod-b  simple CSV record parsing/validation  (pure functions, no I/O)
#
# Both are pure and side-effect free, so a child that edits the other module's
# file produces a real, detectable correctness change rather than a silent
# corruption of shared state. The oracle is run independently by the operator.
set -euo pipefail

BASE="${1:?usage: build-task-fixture.sh <basedir>}"
TASK="$BASE/task"
rm -rf "$TASK"
mkdir -p "$TASK/src" "$TASK/tests"

# ---------------------------------------------------------------- module A
cat > "$TASK/src/mod_a.py" <<'PY'
"""Module A: text normalisation and token statistics.

CONTRACT (do not change the function names or signatures):
  normalise(text) -> str
  token_counts(text) -> dict[str, int]
"""


def normalise(text):
    """Lowercase, strip surrounding whitespace, collapse internal runs of
    whitespace to a single space. Non-string input raises TypeError."""
    raise NotImplementedError


def token_counts(text):
    """Return a mapping of token -> occurrence count over the NORMALISED text.
    Tokens are whitespace-separated. Empty input yields an empty dict."""
    raise NotImplementedError
PY

# ---------------------------------------------------------------- module B
cat > "$TASK/src/mod_b.py" <<'PY'
"""Module B: CSV record parsing and validation.

CONTRACT (do not change the function names or signatures):
  parse_records(text) -> list[dict]
  total_amount(records) -> int
"""

FIELDS = ("id", "name", "amount")


def parse_records(text):
    """Parse CSV text with header line 'id,name,amount'. Return a list of dicts
    with those three keys and amount coerced to int. Skip blank lines. A row
    whose amount is not an integer raises ValueError naming the line number."""
    raise NotImplementedError


def total_amount(records):
    """Sum the amount values. Returns 0 for an empty list."""
    raise NotImplementedError
PY

touch "$TASK/src/__init__.py"

# ------------------------------------------------------- shared test oracle
cat > "$TASK/tests/test_oracle.py" <<'PY'
"""Independent correctness oracle for both modules.

Run with:  python3 -I -m pytest tests/test_oracle.py -q
       or:  python3 -I tests/test_oracle.py      (stdlib fallback, no pytest)

These tests are the SAME for every experimental cell. Neither module may be
changed to make a test pass; the contract above is fixed.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mod_a import normalise, token_counts          # noqa: E402
from mod_b import parse_records, total_amount      # noqa: E402

# ---- module A: normalisation -------------------------------------------------
NORMALISE_CASES = [
    ("  Hello   World  ", "hello world"),
    ("Mixed\tCASE\n\nText", "mixed case text"),
    ("", ""),
    ("   ", ""),
    ("already normal", "already normal"),
    ("Ünïcödé  Ünïcödé", "ünïcödé ünïcödé"),
    ("tabs\tand\tspaces", "tabs and spaces"),
]

# ---- module A: token counting ------------------------------------------------
TOKEN_CASES = [
    ("a b a c a", {"a": 3, "b": 1, "c": 1}),
    ("", {}),
    ("one", {"one": 1}),
    ("same same same", {"same": 3}),
    ("  spaced   out  words ", {"spaced": 1, "out": 1, "words": 1}),
]

# ---- module B: parsing -------------------------------------------------------
GOOD_CSV = "id,name,amount\n1,alice,10\n2,bob,25\n\n3,carol,7\n"
BAD_AMOUNT_CSV = "id,name,amount\n1,alice,notanumber\n"

failures = []


def check(label, got, want):
    if got != want:
        failures.append("%s: got %r want %r" % (label, got, want))


for _in, _want in NORMALISE_CASES:
    try:
        check("normalise(%r)" % _in, normalise(_in), _want)
    except Exception as exc:                       # noqa: BLE001
        failures.append("normalise(%r) raised %r" % (_in, exc))

for _in, _want in TOKEN_CASES:
    try:
        check("token_counts(%r)" % _in, token_counts(_in), _want)
    except Exception as exc:                       # noqa: BLE001
        failures.append("token_counts(%r) raised %r" % (_in, exc))

# malformed input must raise TypeError, not silently coerce
for _bad in (None, 42, ["a"], {"a": 1}):
    try:
        normalise(_bad)
        failures.append("normalise(%r) did not raise TypeError" % (_bad,))
    except TypeError:
        pass
    except Exception as exc:                       # noqa: BLE001
        failures.append("normalise(%r) raised %r not TypeError" % (_bad, exc))

try:
    _recs = parse_records(GOOD_CSV)
    check("parse_records len", len(_recs), 3)
    check("parse_records[0]", _recs[0], {"id": "1", "name": "alice", "amount": 10})
    check("parse_records[2]", _recs[2], {"id": "3", "name": "carol", "amount": 7})
    check("total_amount", total_amount(_recs), 42)
    check("total_amount empty", total_amount([]), 0)
except Exception as exc:                           # noqa: BLE001
    failures.append("parse_records/total_amount raised %r" % (exc,))

# malformed amount must raise ValueError naming the line number
try:
    parse_records(BAD_AMOUNT_CSV)
    failures.append("parse_records(BAD_AMOUNT_CSV) did not raise ValueError")
except ValueError:
    pass
except Exception as exc:                           # noqa: BLE001
    failures.append("parse_records(BAD_AMOUNT_CSV) raised %r not ValueError" % (exc,))

if failures:
    print("ORACLE FAIL (%d)" % len(failures))
    for _f in failures:
        print("  -", _f)
    sys.exit(1)
print("ORACLE PASS")
sys.exit(0)
PY

# ---------------------------------------------------------------- task text
# TASK.md lives INSIDE the task tree so that every per-cell copy carries the
# identical task text. It was previously written to $BASE/TASK.md, outside the
# tree the driver copies, so the cells ran without it.
cat > "$TASK/TASK.md" <<'MD'
# Medium task — two independent modules

Implement the two stub functions in `src/mod_a.py` and `src/mod_b.py`.

The contract for each function is in its module docstring. The docstrings are
the specification; do not change function names, signatures, or the module
docstrings.

`src/__init__.py` is intentionally empty.

## Correctness

`tests/test_oracle.py` is the shared oracle. It must exit 0. It covers
normalisation, token counting, CSV parsing, the malformed-amount ValueError,
and TypeError on non-string input.

Do not weaken, skip or edit any test to make it pass. Do not add files outside
`src/`.

## Modules are independent

`mod_a.py` and `mod_b.py` share no imports and no state. Either may be
implemented without reading the other.
MD

echo "TASK_FIXTURE=$TASK"
find "$TASK" -type f | LC_ALL=C sort
