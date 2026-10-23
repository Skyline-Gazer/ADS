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
