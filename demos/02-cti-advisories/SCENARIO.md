# Demo 02 - Threat advisories as JSON, exported to CSV

**Where the data came from.** A threat-intelligence team publishes advisories as
JSON records (`title`, `date`, `source`, `tags`, `text`). The three here cover a
commodity malware loader, credential stuffing against customer login, and
compromised-build-dependency supply-chain risk. They describe behavior and
defenses only - no fabricated technical indicators.

**What to expect.** An analyst wants to pull advisories relevant to a topic and
hand a tidy table to a spreadsheet or ticketing tool. The new `--format csv`
emits one row per ranked result with a header.

**Run it.**

```bash
cd demos/02-cti-advisories
docarchive index docs --out cti.index.json
docarchive search cti.index.json "credential stuffing multi-factor" --format csv
docarchive search cti.index.json "supply chain dependency" --tag supply-chain --format csv
```

**How to act.** The CSV output opens directly in a spreadsheet; the `tags`
column is semicolon-joined so each result stays on one row. Save it with a
redirect (`... --format csv > hits.csv`) to attach to a ticket.
