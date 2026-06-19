"""Query, ranking (TF-IDF), filtering, and snippet generation.

TF-IDF RANKING FORMULA
----------------------
For a query Q (a set of unique query terms) and a document d, the score is the
sum over query terms t present in d of:

    score(d, Q) = sum_{t in Q} tf_weight(t, d) * idf(t)

where, with N = total number of documents and df(t) = number of documents
containing term t:

    tf_weight(t, d) = 1 + log10( tf(t, d) )          (sublinear term frequency)
    idf(t)          = log10( (N + 1) / (df(t) + 1) ) + 1   (smoothed inverse df)

The sublinear ``tf`` damps the effect of very frequent terms; the smoothed
``idf`` (the "+1" smoothing avoids division by zero and never goes negative)
rewards rarer, more discriminative terms. Only documents containing at least
one query term are returned. Scores are comparable within a single index.
"""

from __future__ import annotations

import math
import re
from typing import Any

from .tokenizer import normalize, tokenize


def _idf(num_docs: int, df: int) -> float:
    return math.log10((num_docs + 1) / (df + 1)) + 1.0


def _tf_weight(tf: int) -> float:
    if tf <= 0:
        return 0.0
    return 1.0 + math.log10(tf)


def _passes_filters(
    doc: dict[str, Any], tag: str | None, since: str | None
) -> bool:
    if tag is not None:
        if tag.lower() not in {t.lower() for t in doc.get("tags", [])}:
            return False
    if since is not None:
        date = doc.get("date") or ""
        # ISO-8601 (YYYY-MM-DD) dates compare correctly as strings.
        if not date or date < since:
            return False
    return True


def make_snippet(
    text: str, query_terms: list[str], *, width: int = 240
) -> str:
    """Build a snippet centered on the first query-term match, with **highlights**.

    Matching is case-insensitive on whole tokens. The first matched query term
    determines the window; all query-term occurrences within the window are
    wrapped in ``**``. If no term matches, the leading slice of text is returned.
    """
    if not text:
        return ""
    terms = {t for t in query_terms if t}
    lowered = text.lower()

    first_pos = None
    if terms:
        # Whole-word search for any query term.
        pattern = re.compile(
            r"\b(" + "|".join(re.escape(t) for t in sorted(terms, key=len, reverse=True)) + r")\b"
        )
        m = pattern.search(lowered)
        if m:
            first_pos = m.start()

    if first_pos is None:
        snippet = text[:width].strip()
        suffix = "..." if len(text) > width else ""
        return snippet + suffix

    half = width // 2
    start = max(0, first_pos - half)
    end = min(len(text), start + width)
    window = text[start:end]

    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(text) else ""

    # Highlight occurrences within the window (operate on original-case slice).
    hl_pattern = re.compile(
        r"\b(" + "|".join(re.escape(t) for t in sorted(terms, key=len, reverse=True)) + r")\b",
        re.IGNORECASE,
    )
    highlighted = hl_pattern.sub(lambda mo: f"**{mo.group(0)}**", window)
    return (prefix + highlighted.strip() + suffix).strip()


def search(
    index: dict[str, Any],
    query: str,
    *,
    tag: str | None = None,
    since: str | None = None,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Run a ranked query against an index.

    Returns a list of result dicts ordered by descending score::

        {"id","title","date","source","tags","score","snippet"}

    ``tag`` filters to documents carrying that tag (case-insensitive).
    ``since`` keeps documents whose ``date`` >= the given ISO date string.
    """
    documents: list[dict[str, Any]] = index["documents"]
    postings: dict[str, dict[str, int]] = index["postings"]
    num_docs: int = index["num_docs"]

    query_terms = tokenize(query)
    if not query_terms:
        return []

    # Unique terms, but preserve query phrasing for snippet matching.
    unique_terms = list(dict.fromkeys(query_terms))

    scores: dict[int, float] = {}
    for term in unique_terms:
        bucket = postings.get(term)
        if not bucket:
            continue
        df = len(bucket)
        idf = _idf(num_docs, df)
        for di_key, tf in bucket.items():
            di = int(di_key)
            scores[di] = scores.get(di, 0.0) + _tf_weight(tf) * idf

    if not scores:
        return []

    # Apply filters and assemble results.
    results: list[dict[str, Any]] = []
    # Snippet highlighting should also catch stopword query terms if the user
    # typed them, so derive a raw lowercased word list from the query.
    raw_query_words = [w for w in normalize(query).split() if w]
    snippet_terms = list(dict.fromkeys(unique_terms + raw_query_words))

    for di, score in scores.items():
        doc = documents[di]
        if not _passes_filters(doc, tag, since):
            continue
        results.append(
            {
                "id": doc["id"],
                "title": doc["title"],
                "date": doc.get("date", ""),
                "source": doc.get("source", ""),
                "tags": doc.get("tags", []),
                "score": round(score, 6),
                "snippet": make_snippet(doc.get("snippet_text", ""), snippet_terms),
            }
        )

    # Sort by score desc, then by id for deterministic tie-breaking.
    results.sort(key=lambda r: (-r["score"], r["id"]))
    if limit and limit > 0:
        results = results[:limit]
    return results
