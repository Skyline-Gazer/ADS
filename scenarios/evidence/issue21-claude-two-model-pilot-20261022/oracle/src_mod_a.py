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
