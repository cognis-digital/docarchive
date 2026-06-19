# docarchive

**Structured archive indexer + full-text search for collections of public records and documents.**

`docarchive` ingests a folder of text, markdown, or JSON documents
(declassified summaries, advisories, analytical reports), builds a searchable
inverted index with metadata (title, date, source, tags), and answers ranked
full-text queries with TF-IDF scoring, date/tag filters, and snippet
highlighting. It runs entirely locally with **no network access** and depends
only on the Python standard library.

Scope is defensive and analytical: organizing, indexing, and searching
document collections you already hold.

---

## Install

Requires Python 3.10+.

```bash
git clone <your-fork-url> docarchive
cd docarchive
pip install -e .
```

This installs the `docarchive` console command. For development/tests:

```bash
pip install -e ".[test]"
```

---

## Usage

### 1. Build an index

```console
$ docarchive index examples --out examples.index.json
Indexed 4 document(s), 187 unique term(s) -> examples.index.json
```

### 2. Search

```console
$ docarchive search examples.index.json "grid resilience"
1. Advisory on Grid Resilience During Peak Demand  (score 5.8124)
   id: advisory-power-grid.md  [2026-03-14 | Cognis Digital Analytical Notes | tags: energy, infrastructure, resilience]
   ...Operators of regional transmission networks should review contingency plans ahead of sustained peak-demand windows... controlled load curtailment is preferable to uncontrolled cascading outages...
```

Filter by tag, by date, and emit JSON:

```console
$ docarchive search examples.index.json "minerals" --tag supply-chain
1. Critical Minerals Supply Chain Overview  (score 2.6021)
   id: report-supply-chain.txt  [2026-01-22 | Cognis Digital Analytical Notes | tags: economics, minerals, supply-chain]
   Critical **minerals** underpin modern manufacturing, from batteries to magnets...

$ docarchive search examples.index.json "osint methods" --since 2026-02-01 --json
[
  {
    "id": "note-osint-methods.md",
    "title": "Open-Source Intelligence Methods for Analysts",
    "date": "2026-02-19",
    "source": "Cognis Digital Analytical Notes",
    "tags": ["methods", "osint", "research"],
    "score": 4.812345,
    "snippet": "Open-source intelligence relies only on publicly available information..."
  }
]
```

### 3. Stats

```console
$ docarchive stats examples.index.json
Documents:     4
Unique terms:  187
Total tokens:  263
Date range:    2025-11-08 .. 2026-03-14
Tags:
  atmosphere: 1
  economics: 1
  energy: 1
  history: 1
  infrastructure: 1
  methods: 1
  minerals: 1
  osint: 1
  research: 2
  resilience: 1
  supply-chain: 1
```

---

## Document formats

* **`.txt` / `.md`** — plain or markdown text. Optional front matter delimited by
  `---` lines at the top of the file supplies metadata:

  ```markdown
  ---
  title: My Report
  date: 2026-03-14
  source: Cognis Digital Analytical Notes
  tags: energy, resilience
  ---
  Body text follows...
  ```

  If no `title` is given, the first non-empty line (with a leading `#` stripped)
  is used.

* **`.json`** — an object with the body under `text`, `body`, or `content`, plus
  optional `title`, `date`, `source`, and `tags` (string or array).

Dates are stored as given; ISO-8601 (`YYYY-MM-DD`) sorts and filters correctly.

---

## Features

- Recursive ingest of `.txt`, `.md`, and `.json` documents with metadata.
- Inverted index with term postings, term frequencies, and document frequencies.
- TF-IDF ranking implemented from scratch (formula below).
- Authored tokenizer with a compact, project-original English stopword list and
  hyphenated-token support.
- Ranked search with score, metadata, and highlighted snippets centered on the
  first match.
- `--tag`, `--since`, `--limit`, and `--json` query options.
- `stats` summary: document count, unique terms, token total, date range, tags.
- Standard library only. Real pytest suite covering tokenizing, indexing,
  ranking order, filters, snippets, and the CLI.

---

## Ranking formula

For a query `Q` (its set of unique terms) and document `d`, the relevance score
is the sum over query terms `t` that occur in `d`:

```
score(d, Q) = sum over t in Q of  tf_weight(t, d) * idf(t)
```

With `N` = total number of documents and `df(t)` = number of documents
containing term `t`:

```
tf_weight(t, d) = 1 + log10( tf(t, d) )            # sublinear term frequency
idf(t)          = log10( (N + 1) / (df(t) + 1) ) + 1   # smoothed inverse document frequency
```

The sublinear `tf` damps the influence of terms repeated many times within one
document; the smoothed `idf` (with `+1` smoothing in numerator and denominator)
avoids division by zero, stays non-negative, and rewards rarer, more
discriminative terms. Only documents containing at least one query term are
returned. Scores are comparable within a single index. Ties break by document
id for deterministic ordering.

---

## License

License: COCL 1.0

---

Maintained by **Cognis Digital**.
