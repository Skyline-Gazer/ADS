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
