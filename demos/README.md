# docarchive demos

Each folder is a self-contained, real-use-case walkthrough: a `docs/` directory
of documents in docarchive's real input formats (`.md`/`.txt` with front matter,
or `.json`) plus a `SCENARIO.md` explaining where the data came from, what to
expect, the exact commands, and how to act on the results.

All content is defensive/analytical and uses only synthetic or
behaviorally-described material - no fabricated CVE IDs, hashes, or fingerprints.

Run any demo from its folder once `docarchive` is installed (`pip install -e .`),
or from the repo root without installing via
`PYTHONPATH=src python -m docarchive ...`.

| # | Demo | Formats | Highlights |
|---|------|---------|-----------|
| 01 | [SOC incident-response runbooks](01-ir-runbooks/) | `.md` | ranked search, `--tag` filter |
| 02 | [Threat-intelligence advisories](02-cti-advisories/) | `.json` | `--format csv` export |
| 03 | [Coordinated vulnerability disclosures](03-vuln-disclosures/) | `.md`, `.txt` | search by vuln class, `--tag` |
| 04 | [Public-records (FOIA-style) collection](04-foia-records/) | `.txt`, `.json` | `stats` overview |
| 05 | [OSINT analyst notebook](05-osint-field-notes/) | `.md` | `--format ndjson` streaming |
| 06 | [Secure code-review findings](06-appsec-findings/) | `.json` | CSV export for trackers |
| 07 | [Firmware analysis lab notes](07-firmware-notes/) | `.md`, `.txt` | weakness-class search |
| 08 | [Security governance minutes](08-board-minutes/) | `.md`, `.json` | `--since` date scoping |

## Quick start

```bash
cd demos/01-ir-runbooks
docarchive index docs --out runbooks.index.json
docarchive search runbooks.index.json "ransomware containment backups"
```
