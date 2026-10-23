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
