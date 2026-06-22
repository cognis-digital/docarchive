# Demo 05 - OSINT analyst notebook, streamed as NDJSON

**Where the data came from.** A defensive OSINT analyst keeps field notes as
markdown with front matter: lookalike-domain monitoring, an employee credential
exposure check against public breach data, and an external attack-surface
inventory. Every method uses only publicly available information.

**What to expect.** The analyst wants to feed matching notes into a log/event
pipeline (jq, an Elastic ingest, etc.), where newline-delimited JSON is the
natural shape. The new `--format ndjson` prints one compact JSON object per line.

**Run it.**

```bash
cd demos/05-osint-field-notes
docarchive index docs --out notebook.index.json
docarchive search notebook.index.json "domain phishing impersonation" --format ndjson
docarchive search notebook.index.json "attack surface inventory" --format ndjson | python -c "import sys,json;[print(json.loads(l)['title']) for l in sys.stdin]"
```

**How to act.** Each NDJSON line is independently parseable, so you can pipe the
stream straight into `jq` or a bulk indexer. The first query surfaces the
lookalike-domain note as the top hit.
