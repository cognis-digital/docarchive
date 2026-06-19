"""Index statistics."""

from __future__ import annotations

from typing import Any


def compute_stats(index: dict[str, Any]) -> dict[str, Any]:
    """Summarize an index: doc count, unique terms, date range, tag counts."""
    documents: list[dict[str, Any]] = index["documents"]
    postings: dict[str, Any] = index["postings"]

    dates = sorted(d["date"] for d in documents if d.get("date"))
    tag_counts: dict[str, int] = {}
    total_tokens = 0
    for d in documents:
        total_tokens += int(d.get("length", 0))
        for t in d.get("tags", []):
            tag_counts[t] = tag_counts.get(t, 0) + 1

    return {
        "num_docs": len(documents),
        "num_terms": len(postings),
        "total_tokens": total_tokens,
        "date_min": dates[0] if dates else None,
        "date_max": dates[-1] if dates else None,
        "tags": dict(sorted(tag_counts.items())),
    }
