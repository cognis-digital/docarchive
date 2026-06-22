"""Output serializers for search results.

``docarchive search`` can emit ranked results in several formats so they can be
piped into spreadsheets, log pipelines, or other tooling without any extra
dependencies:

* ``text``   - the human-readable ranked listing (handled by the CLI).
* ``json``   - a pretty-printed JSON array (handled by the CLI).
* ``csv``    - one row per result, RFC-4180 style, header included. Suitable for
               opening in a spreadsheet or feeding a data pipeline.
* ``ndjson`` - newline-delimited JSON: one compact JSON object per line. Ideal
               for streaming into log/event processors (jq, Splunk, Elastic).

All serializers operate on the result dicts produced by
:func:`docarchive.search.search`, i.e. dicts with keys
``id, title, date, source, tags, score, snippet``.
"""

from __future__ import annotations

import csv
import io
import json
from typing import Any

# Stable column order for tabular (CSV) output.
CSV_COLUMNS = ["rank", "id", "title", "date", "source", "tags", "score", "snippet"]

VALID_FORMATS = ("text", "json", "csv", "ndjson")


def to_csv(results: list[dict[str, Any]]) -> str:
    """Serialize results to RFC-4180 CSV text (with a header row).

    ``tags`` (a list) is rendered as a semicolon-separated string so each result
    stays on a single row. ``rank`` is a 1-based position reflecting the ranked
    order of ``results``.
    """
    buf = io.StringIO()
    # newline="" semantics: csv writes \r\n; we keep that for RFC-4180 fidelity.
    writer = csv.DictWriter(buf, fieldnames=CSV_COLUMNS, extrasaction="ignore")
    writer.writeheader()
    for rank, r in enumerate(results, start=1):
        writer.writerow(
            {
                "rank": rank,
                "id": r.get("id", ""),
                "title": r.get("title", ""),
                "date": r.get("date", ""),
                "source": r.get("source", ""),
                "tags": ";".join(r.get("tags", []) or []),
                "score": r.get("score", ""),
                "snippet": r.get("snippet", ""),
            }
        )
    return buf.getvalue()


def to_ndjson(results: list[dict[str, Any]]) -> str:
    """Serialize results to newline-delimited JSON (one object per line).

    A trailing newline is included so the output is a well-formed NDJSON stream
    that concatenates cleanly. An empty result set yields an empty string.
    """
    if not results:
        return ""
    lines = [json.dumps(r, ensure_ascii=False, sort_keys=True) for r in results]
    return "\n".join(lines) + "\n"
