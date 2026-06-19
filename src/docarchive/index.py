"""Index construction: ingest documents and build an inverted index.

Supported document formats in a docs directory:

* ``.txt`` / ``.md`` - plain/markdown text. Metadata may optionally be supplied
  via a YAML-ish front-matter block delimited by ``---`` lines at the top of the
  file (a tiny key: value parser, no external YAML dependency). Recognized keys:
  ``title``, ``date``, ``source``, ``tags`` (comma-separated). If no title is
  given, the first non-empty line (with a leading ``#`` stripped) is used.
* ``.json`` - an object with ``text``/``body``/``content`` for the body and any
  of ``title``, ``date``, ``source``, ``tags`` for metadata.

The produced index is a plain JSON-serializable dict (see ``build_index``).
"""

from __future__ import annotations

import json
import os
from typing import Any

from .tokenizer import tokenize

INDEX_FORMAT_VERSION = 1
_FRONT_MATTER_KEYS = {"title", "date", "source", "tags"}


def _parse_tags(value: Any) -> list[str]:
    """Normalize a tags value into a sorted, de-duplicated lowercase list."""
    if value is None:
        return []
    if isinstance(value, str):
        parts = [p.strip() for p in value.split(",")]
    elif isinstance(value, (list, tuple)):
        parts = [str(p).strip() for p in value]
    else:
        parts = [str(value).strip()]
    seen: dict[str, None] = {}
    for p in parts:
        if p:
            seen[p.lower()] = None
    return sorted(seen)


def _parse_front_matter(text: str) -> tuple[dict[str, Any], str]:
    """Extract an optional ``---`` delimited front-matter block.

    Returns ``(metadata, body)``. If no valid front matter is present the
    metadata dict is empty and body is the original text.
    """
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    # First line must be exactly '---' (allowing trailing whitespace).
    if lines[0].strip() != "---":
        return {}, text
    meta: dict[str, Any] = {}
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
        line = lines[i]
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip().lower()
            if key in _FRONT_MATTER_KEYS:
                meta[key] = val.strip()
    if end is None:
        # No closing delimiter; treat whole thing as body.
        return {}, text
    body = "\n".join(lines[end + 1 :])
    return meta, body


def _first_title(body: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped.lstrip("#").strip()
    return ""


def _load_document(path: str) -> dict[str, Any] | None:
    """Read a single file and return a normalized document dict, or None.

    Returns dict with keys: id, title, date, source, tags (list), body (str).
    Returns None for unsupported/unreadable files.
    """
    ext = os.path.splitext(path)[1].lower()
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = fh.read()
    except (OSError, UnicodeDecodeError):
        return None

    doc_id = os.path.basename(path)

    if ext == ".json":
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            return None
        if not isinstance(obj, dict):
            return None
        body = ""
        for key in ("text", "body", "content"):
            if isinstance(obj.get(key), str):
                body = obj[key]
                break
        title = str(obj.get("title") or "").strip() or _first_title(body) or doc_id
        return {
            "id": doc_id,
            "title": title,
            "date": str(obj.get("date") or "").strip(),
            "source": str(obj.get("source") or "").strip(),
            "tags": _parse_tags(obj.get("tags")),
            "body": body,
        }

    if ext in (".txt", ".md"):
        meta, body = _parse_front_matter(raw)
        title = str(meta.get("title") or "").strip() or _first_title(body) or doc_id
        return {
            "id": doc_id,
            "title": title,
            "date": str(meta.get("date") or "").strip(),
            "source": str(meta.get("source") or "").strip(),
            "tags": _parse_tags(meta.get("tags")),
            "body": body,
        }

    return None


def iter_document_paths(docs_dir: str) -> list[str]:
    """Return sorted supported document paths under ``docs_dir`` (recursive)."""
    paths: list[str] = []
    for root, _dirs, files in os.walk(docs_dir):
        for name in files:
            if os.path.splitext(name)[1].lower() in (".txt", ".md", ".json"):
                paths.append(os.path.join(root, name))
    return sorted(paths)


def build_index(docs_dir: str) -> dict[str, Any]:
    """Build an inverted index over all supported documents in ``docs_dir``.

    Index schema::

        {
          "format_version": 1,
          "documents": [
            {"id","title","date","source","tags","length","snippet_text"}, ...
          ],
          "postings": { term: { doc_index: term_frequency, ... }, ... },
          "doc_freq": { term: number_of_docs_containing_term },
          "num_docs": int
        }

    ``doc_index`` keys in postings are stringified integer indices into the
    ``documents`` list (JSON object keys must be strings).
    """
    if not os.path.isdir(docs_dir):
        raise NotADirectoryError(f"not a directory: {docs_dir}")

    documents: list[dict[str, Any]] = []
    postings: dict[str, dict[str, int]] = {}
    doc_freq: dict[str, int] = {}

    for path in iter_document_paths(docs_dir):
        doc = _load_document(path)
        if doc is None:
            continue
        # Index over title + body so titles are searchable and weighted.
        indexable = f"{doc['title']}\n{doc['body']}"
        tokens = tokenize(indexable)

        term_counts: dict[str, int] = {}
        for tok in tokens:
            term_counts[tok] = term_counts.get(tok, 0) + 1

        doc_index = len(documents)
        documents.append(
            {
                "id": doc["id"],
                "title": doc["title"],
                "date": doc["date"],
                "source": doc["source"],
                "tags": doc["tags"],
                "length": len(tokens),
                # Store a trimmed copy of the body for snippet generation.
                "snippet_text": doc["body"].strip(),
            }
        )

        di_key = str(doc_index)
        for term, count in term_counts.items():
            bucket = postings.get(term)
            if bucket is None:
                bucket = {}
                postings[term] = bucket
            bucket[di_key] = count
            doc_freq[term] = doc_freq.get(term, 0) + 1

    return {
        "format_version": INDEX_FORMAT_VERSION,
        "documents": documents,
        "postings": postings,
        "doc_freq": doc_freq,
        "num_docs": len(documents),
    }


def save_index(index: dict[str, Any], out_path: str) -> None:
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(index, fh, ensure_ascii=False, separators=(",", ":"))


def load_index(in_path: str) -> dict[str, Any]:
    with open(in_path, "r", encoding="utf-8") as fh:
        index = json.load(fh)
    if not isinstance(index, dict) or "postings" not in index:
        raise ValueError(f"not a valid docarchive index: {in_path}")
    return index
