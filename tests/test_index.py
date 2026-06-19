import json
import os

import pytest

from docarchive.index import build_index, load_index, save_index


def test_index_counts(index):
    assert index["num_docs"] == 3
    assert index["format_version"] == 1
    assert index["postings"]  # non-empty


def test_metadata_parsed_front_matter(index):
    docs = {d["id"]: d for d in index["documents"]}
    grid = docs["grid.md"]
    assert grid["title"] == "Grid Resilience"
    assert grid["date"] == "2026-03-14"
    assert grid["source"] == "Notes"
    assert grid["tags"] == ["energy", "resilience"]


def test_metadata_parsed_json(index):
    docs = {d["id"]: d for d in index["documents"]}
    balloon = docs["balloon.json"]
    assert balloon["title"] == "Weather Balloon"
    assert balloon["tags"] == ["history", "research"]


def test_term_frequency_recorded(index):
    # "resilience" appears multiple times in grid.md
    postings = index["postings"]
    assert "resilience" in postings
    # exactly one doc contains it -> doc_freq 1
    assert index["doc_freq"]["resilience"] == 1
    tf = list(postings["resilience"].values())[0]
    assert tf >= 4


def test_stopwords_not_indexed(index):
    assert "the" not in index["postings"]
    assert "and" not in index["postings"]


def test_save_and_load_roundtrip(index, tmp_path):
    out = str(tmp_path / "idx.json")
    save_index(index, out)
    assert os.path.exists(out)
    reloaded = load_index(out)
    assert reloaded["num_docs"] == index["num_docs"]
    assert reloaded["postings"] == index["postings"]


def test_load_invalid_index_raises(tmp_path):
    bad = str(tmp_path / "bad.json")
    with open(bad, "w", encoding="utf-8") as fh:
        json.dump({"not": "an index"}, fh)
    with pytest.raises(ValueError):
        load_index(bad)


def test_build_index_missing_dir():
    with pytest.raises(NotADirectoryError):
        build_index("/no/such/directory/here")
