# Demo 03 - Coordinated disclosure records (mixed formats)

**Where the data came from.** An application-security team logs coordinated,
authorized vulnerability disclosures as a mix of markdown and text files with
front matter. The three here document an IDOR in a reporting API, stored XSS in
a comment field, and SSRF in a thumbnail fetcher. Each describes impact, root
cause, and remediation. No CVE identifiers or hashes are fabricated.

**What to expect.** A reviewer searching by vulnerability class should land on
the matching disclosure, and a tag filter should isolate a class (e.g. `ssrf`).

**Run it.**

```bash
cd demos/03-vuln-disclosures
docarchive index docs --out disclosures.index.json
docarchive search disclosures.index.json "ssrf internal metadata"
docarchive search disclosures.index.json "authorization tenant" --tag idor
```

**How to act.** The SSRF query returns the thumbnail-fetcher disclosure first;
use its remediation (allowlist destinations, deny private ranges) as the pattern
for similar endpoints. The tag query confirms which disclosures are IDOR-class.
