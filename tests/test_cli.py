import json

from docarchive.cli import main


def test_cli_index_search_stats(tmp_path, capsys):
    import os

    docs = tmp_path / "docs"
    docs.mkdir()
    with open(docs / "a.md", "w", encoding="utf-8") as fh:
        fh.write(
            "---\ntitle: Alpha Report\ndate: 2026-01-01\ntags: alpha\n---\n"
            "The alpha report discusses resilience and resilience again.\n"
        )
    idx = tmp_path / "index.json"

    rc = main(["index", str(docs), "--out", str(idx)])
    assert rc == 0
    assert idx.exists()
    capsys.readouterr()  # drop the index summary line

    rc = main(["search", str(idx), "resilience", "--json"])
    assert rc == 0
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data[0]["id"] == "a.md"

    rc = main(["stats", str(idx), "--json"])
    assert rc == 0
    out = capsys.readouterr().out
    s = json.loads(out)
    assert s["num_docs"] == 1


def test_cli_search_text_output(tmp_path, capsys):
    docs = tmp_path / "docs"
    docs.mkdir()
    with open(docs / "b.md", "w", encoding="utf-8") as fh:
        fh.write("---\ntitle: Beta\ndate: 2026-02-02\n---\nBeta covers minerals supply.\n")
    idx = tmp_path / "i.json"
    main(["index", str(docs), "--out", str(idx)])
    capsys.readouterr()
    rc = main(["search", str(idx), "minerals"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Beta" in out
    assert "score" in out


def test_cli_missing_dir_returns_error(tmp_path, capsys):
    rc = main(["index", str(tmp_path / "missing"), "--out", str(tmp_path / "x.json")])
    assert rc == 2
