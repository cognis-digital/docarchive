"""Guard tests: every shipped demo indexes cleanly and is searchable.

These keep the demos/ walkthroughs honest - if a demo document stops parsing or
a demo folder is emptied, the suite fails instead of shipping a broken example.
"""

import os

import pytest

from docarchive.index import build_index
from docarchive.search import search

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEMOS_DIR = os.path.join(REPO_ROOT, "demos")


def _demo_doc_dirs():
    if not os.path.isdir(DEMOS_DIR):
        return []
    out = []
    for name in sorted(os.listdir(DEMOS_DIR)):
        docs = os.path.join(DEMOS_DIR, name, "docs")
        if os.path.isdir(docs):
            out.append((name, docs))
    return out


DEMO_DIRS = _demo_doc_dirs()


def test_demos_present():
    # We ship a known set of demos; ensure none silently vanished.
    assert len(DEMO_DIRS) >= 8


@pytest.mark.parametrize("name,docs", DEMO_DIRS, ids=[d[0] for d in DEMO_DIRS])
def test_demo_indexes_and_searches(name, docs):
    index = build_index(docs)
    assert index["num_docs"] >= 1, f"{name}: no documents indexed"
    assert index["postings"], f"{name}: empty index"
    # Every indexed doc must carry a title and contribute a snippet source.
    for doc in index["documents"]:
        assert doc["title"], f"{name}: doc {doc['id']} has no title"
    # A search for a common defensive term returns ranked results in at least
    # one demo; here we just confirm the index is queryable without error.
    results = search(index, "the and authorized review", limit=5)
    assert isinstance(results, list)


@pytest.mark.parametrize("name,docs", DEMO_DIRS, ids=[d[0] for d in DEMO_DIRS])
def test_demo_has_scenario(name, docs):
    scenario = os.path.join(os.path.dirname(docs), "SCENARIO.md")
    assert os.path.isfile(scenario), f"{name}: missing SCENARIO.md"
