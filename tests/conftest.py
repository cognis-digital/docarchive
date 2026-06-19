import json
import os

import pytest

from docarchive.index import build_index


def _write(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


@pytest.fixture()
def docs_dir(tmp_path):
    d = tmp_path / "docs"
    d.mkdir()

    _write(
        str(d / "grid.md"),
        "---\n"
        "title: Grid Resilience\n"
        "date: 2026-03-14\n"
        "source: Notes\n"
        "tags: energy, resilience\n"
        "---\n"
        "Grid resilience depends on reserve margin and controlled curtailment. "
        "Resilience resilience resilience of the grid matters.\n",
    )
    _write(
        str(d / "minerals.txt"),
        "---\n"
        "title: Minerals Supply Chain\n"
        "date: 2026-01-22\n"
        "source: Notes\n"
        "tags: minerals, economics\n"
        "---\n"
        "Critical minerals underpin manufacturing and supply chain security.\n",
    )
    _write(
        str(d / "balloon.json"),
        json.dumps(
            {
                "title": "Weather Balloon",
                "date": "2025-11-08",
                "source": "Archive",
                "tags": ["history", "research"],
                "text": "A weather balloon carried instruments to measure the upper atmosphere.",
            }
        ),
    )
    return str(d)


@pytest.fixture()
def index(docs_dir):
    return build_index(docs_dir)
