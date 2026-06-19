"""Tokenization and stopword handling.

Tokenization is deliberately simple and language-agnostic for English text:
lowercase, split on any non-alphanumeric run, drop very short tokens and
stopwords. The stopword list below is authored for this project (a compact set
of high-frequency English function words); it is not derived from any external
corpus or third-party list.
"""

from __future__ import annotations

import re

# Authored compact English stopword list (function words that carry little
# discriminative signal for full-text ranking).
STOPWORDS: frozenset[str] = frozenset(
    {
        "a", "an", "and", "are", "as", "at", "be", "been", "being", "but",
        "by", "for", "from", "had", "has", "have", "he", "her", "him", "his",
        "i", "if", "in", "into", "is", "it", "its", "of", "on", "or", "our",
        "she", "so", "than", "that", "the", "their", "them", "then", "there",
        "these", "they", "this", "to", "was", "we", "were", "what", "when",
        "which", "who", "will", "with", "would", "you", "your",
    }
)

# A "word" is a run of letters/digits, optionally containing internal hyphens
# or apostrophes (e.g. "counter-uas", "don't"). Surrounding punctuation is
# stripped by the split.
_TOKEN_RE = re.compile(r"[a-z0-9]+(?:[-'][a-z0-9]+)*")

# Minimum length for a token to be kept (drops single characters like "x").
MIN_TOKEN_LEN = 2


def normalize(text: str) -> str:
    """Lowercase text for case-insensitive matching."""
    return text.lower()


def tokenize(text: str, *, keep_stopwords: bool = False) -> list[str]:
    """Split text into normalized tokens.

    Lowercases, extracts alphanumeric word runs, drops tokens shorter than
    ``MIN_TOKEN_LEN`` and (unless ``keep_stopwords``) authored stopwords.
    """
    tokens = _TOKEN_RE.findall(normalize(text))
    out: list[str] = []
    for tok in tokens:
        if len(tok) < MIN_TOKEN_LEN:
            continue
        if not keep_stopwords and tok in STOPWORDS:
            continue
        out.append(tok)
    return out
