from docarchive.search import search, make_snippet


def test_basic_match(index):
    results = search(index, "resilience")
    assert results
    assert results[0]["id"] == "grid.md"


def test_ranking_order_rarer_term_ranks_relevant_doc_first(index):
    # "minerals" only in minerals.txt; "grid" only in grid.md
    results = search(index, "minerals")
    assert results[0]["id"] == "minerals.txt"


def test_repeated_term_boosts_score(index):
    # grid.md has many 'resilience' occurrences; it should outrank others
    results = search(index, "resilience grid")
    assert results[0]["id"] == "grid.md"
    # score is positive
    assert results[0]["score"] > 0


def test_no_match_returns_empty(index):
    assert search(index, "zzzzznotpresent") == []


def test_empty_query_returns_empty(index):
    assert search(index, "the and of") == []  # all stopwords


def test_tag_filter(index):
    results = search(index, "supply minerals balloon", tag="minerals")
    ids = {r["id"] for r in results}
    assert ids == {"minerals.txt"}


def test_since_filter(index):
    # only docs dated >= 2026-02-01
    results = search(index, "resilience minerals balloon atmosphere", since="2026-02-01")
    ids = {r["id"] for r in results}
    assert ids == {"grid.md"}  # 2026-03-14 passes; others earlier


def test_snippet_highlights_query_term(index):
    results = search(index, "balloon")
    snip = results[0]["snippet"]
    assert "**balloon**" in snip.lower() or "**Balloon**" in snip


def test_limit(index):
    results = search(index, "the grid minerals balloon resilience", limit=1)
    assert len(results) == 1


def test_make_snippet_no_match_returns_prefix():
    text = "alpha beta gamma delta " * 20
    snip = make_snippet(text, ["nomatch"], width=40)
    assert snip.startswith("alpha")
    assert snip.endswith("...")


def test_make_snippet_centers_on_match():
    text = "lead in text here " * 10 + "TARGET word " + "trailing text " * 10
    snip = make_snippet(text, ["target"], width=60)
    assert "**TARGET**" in snip
