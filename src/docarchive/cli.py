"""Command-line interface for docarchive."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from . import __version__
from .index import build_index, load_index, save_index
from .search import search as run_search
from .stats import compute_stats


def _cmd_index(args: argparse.Namespace) -> int:
    index = build_index(args.docs_dir)
    save_index(index, args.out)
    print(
        f"Indexed {index['num_docs']} document(s), "
        f"{len(index['postings'])} unique term(s) -> {args.out}"
    )
    return 0


def _print_results(results: list[dict[str, Any]]) -> None:
    if not results:
        print("No matching documents.")
        return
    for rank, r in enumerate(results, start=1):
        meta_bits = []
        if r.get("date"):
            meta_bits.append(r["date"])
        if r.get("source"):
            meta_bits.append(r["source"])
        if r.get("tags"):
            meta_bits.append("tags: " + ", ".join(r["tags"]))
        meta = ("  [" + " | ".join(meta_bits) + "]") if meta_bits else ""
        print(f"{rank}. {r['title']}  (score {r['score']:.4f})")
        print(f"   id: {r['id']}{meta}")
        if r.get("snippet"):
            print(f"   {r['snippet']}")
        print()


def _cmd_search(args: argparse.Namespace) -> int:
    index = load_index(args.index)
    results = run_search(
        index,
        args.query,
        tag=args.tag,
        since=args.since,
        limit=args.limit,
    )
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        _print_results(results)
    return 0


def _cmd_stats(args: argparse.Namespace) -> int:
    index = load_index(args.index)
    s = compute_stats(index)
    if args.json:
        print(json.dumps(s, ensure_ascii=False, indent=2))
        return 0
    print(f"Documents:     {s['num_docs']}")
    print(f"Unique terms:  {s['num_terms']}")
    print(f"Total tokens:  {s['total_tokens']}")
    rng = (
        f"{s['date_min']} .. {s['date_max']}"
        if s["date_min"] or s["date_max"]
        else "(none)"
    )
    print(f"Date range:    {rng}")
    if s["tags"]:
        print("Tags:")
        for tag, count in s["tags"].items():
            print(f"  {tag}: {count}")
    else:
        print("Tags:          (none)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="docarchive",
        description="Structured archive indexer + full-text search for document collections.",
    )
    parser.add_argument(
        "--version", action="version", version=f"docarchive {__version__}"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_index = sub.add_parser("index", help="Build a search index from a docs directory.")
    p_index.add_argument("docs_dir", help="Directory containing .txt/.md/.json documents.")
    p_index.add_argument("--out", default="index.json", help="Output index path (default: index.json).")
    p_index.set_defaults(func=_cmd_index)

    p_search = sub.add_parser("search", help="Search an index with a ranked query.")
    p_search.add_argument("index", help="Path to an index.json built by 'index'.")
    p_search.add_argument("query", help="Query string.")
    p_search.add_argument("--tag", default=None, help="Filter to documents carrying this tag.")
    p_search.add_argument("--since", default=None, help="Keep documents with date >= this ISO date (YYYY-MM-DD).")
    p_search.add_argument("--limit", type=int, default=10, help="Maximum results (default: 10).")
    p_search.add_argument("--json", action="store_true", help="Emit results as JSON.")
    p_search.set_defaults(func=_cmd_search)

    p_stats = sub.add_parser("stats", help="Show statistics about an index.")
    p_stats.add_argument("index", help="Path to an index.json.")
    p_stats.add_argument("--json", action="store_true", help="Emit stats as JSON.")
    p_stats.set_defaults(func=_cmd_stats)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (FileNotFoundError, NotADirectoryError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
