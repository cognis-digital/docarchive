import csv
import io
import json

from docarchive.cli import main
from docarchive.formats import CSV_COLUMNS, to_csv, to_ndjson

SAMPLE = [
    {
        "id": "doc-a.md",
        "title": "Alpha, Beta",  # comma -> must be quoted in CSV
        "date": "2026-01-01",
        "source": "Notes",
        "tags": ["energy", "resilience"],
        "score": 5.8124,
        "snippet": "Line one\nLine two",  # embedded newline -> must be quoted
    },
    {
        "id": "doc-b.md",
        "title": "Gamma",
        "date": "",
        "source": "",
        "tags": [],
        "score": 1.0,
        "snippet": "plain",
    },
]


def test_to_csv_header_and_rows():
    text = to_csv(SAMPLE)
    rows = list(csv.DictReader(io.StringIO(text)))
    assert list(rows[0].keys()) == CSV_COLUMNS
    assert rows[0]["rank"] == "1"
    assert rows[0]["id"] == "doc-a.md"
    # tags rendered as semicolon-joined string, list kept on one row.
    assert rows[0]["tags"] == "energy;resilience"
    # comma in title and newline in snippet survived the round-trip intact.
    assert rows[0]["title"] == "Alpha, Beta"
    assert rows[0]["snippet"] == "Line one\nLine two"
    assert rows[1]["rank"] == "2"
    assert rows[1]["tags"] == ""


def test_to_ndjson_one_object_per_line():
    text = to_ndjson(SAMPLE)
    lines = text.splitlines()
    assert len(lines) == 2
    first = json.loads(lines[0])
    assert first["id"] == "doc-a.md"
    assert first["tags"] == ["energy", "resilience"]


def test_to_ndjson_empty():
    assert to_ndjson([]) == ""


def test_to_csv_empty_has_only_header():
    text = to_csv([])
    rows = list(csv.reader(io.StringIO(text)))
    assert rows == [CSV_COLUMNS]


def _build_index(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    with open(docs / "grid.md", "w", encoding="utf-8") as fh:
        fh.write(
            "---\ntitle: Grid Resilience\ndate: 2026-03-14\n"
            "source: Notes\ntags: energy, resilience\n---\n"
            "Grid resilience depends on reserve margin and curtailment.\n"
        )
    idx = tmp_path / "index.json"
    main(["index", str(docs), "--out", str(idx)])
    return str(idx)


def test_cli_search_csv(tmp_path, capsys):
    idx = _build_index(tmp_path)
    capsys.readouterr()
    rc = main(["search", idx, "resilience", "--format", "csv"])
    assert rc == 0
    out = capsys.readouterr().out
    rows = list(csv.DictReader(io.StringIO(out)))
    assert rows[0]["id"] == "grid.md"
    assert rows[0]["tags"] == "energy;resilience"


def test_cli_search_ndjson(tmp_path, capsys):
    idx = _build_index(tmp_path)
    capsys.readouterr()
    rc = main(["search", idx, "resilience", "--format", "ndjson"])
    assert rc == 0
    out = capsys.readouterr().out
    lines = out.splitlines()
    obj = json.loads(lines[0])
    assert obj["id"] == "grid.md"


def test_cli_json_flag_still_works(tmp_path, capsys):
    idx = _build_index(tmp_path)
    capsys.readouterr()
    rc = main(["search", idx, "resilience", "--json"])
    assert rc == 0
    data = json.loads(capsys.readouterr().out)
    assert data[0]["id"] == "grid.md"
