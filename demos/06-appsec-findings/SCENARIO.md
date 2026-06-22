# Demo 06 - Secure code review findings, tracked and exported

**Where the data came from.** A secure-code-review practice records findings as
JSON: a hardcoded secret in configuration, a missing rate limit on password
reset, and verbose error messages that leak stack traces. Each states impact,
remediation, and an assessed severity.

**What to expect.** A lead wants to rank findings by relevance to a theme and
export the table for a remediation tracker. CSV export gives a spreadsheet-ready
view, with the highest-scoring finding first.

**Run it.**

```bash
cd demos/06-appsec-findings
docarchive index docs --out findings.index.json
docarchive search findings.index.json "secret rate limit enumeration" --format csv
docarchive search findings.index.json "configuration" --tag configuration
```

**How to act.** The CSV top row is the missing-rate-limit finding (highest
score for that query); redirect to a file and import it into your tracker. The
tag query groups the two `configuration`-tagged findings for a config-hardening
sweep.
