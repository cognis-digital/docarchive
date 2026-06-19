from docarchive.stats import compute_stats


def test_stats_counts(index):
    s = compute_stats(index)
    assert s["num_docs"] == 3
    assert s["num_terms"] == len(index["postings"])
    assert s["total_tokens"] > 0


def test_stats_date_range(index):
    s = compute_stats(index)
    assert s["date_min"] == "2025-11-08"
    assert s["date_max"] == "2026-03-14"


def test_stats_tags(index):
    s = compute_stats(index)
    assert s["tags"]["minerals"] == 1
    assert s["tags"]["resilience"] == 1
    assert s["tags"]["research"] == 1
