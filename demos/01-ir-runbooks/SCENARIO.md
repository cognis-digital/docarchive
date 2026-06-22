# Demo 01 - Searching a SOC runbook library

**Where the data came from.** A security operations team keeps its incident
response runbooks as markdown files with front matter (`title`, `date`,
`source`, `tags`). The three runbooks here cover credential phishing, ransomware
containment, and suspected data exfiltration. All content is defensive guidance
for authorized responders.

**What to expect.** During an incident a responder needs the right runbook fast.
A ranked search for the situation should surface the matching runbook first, and
a tag filter should narrow to a category (for example, identity-related
playbooks).

**Run it.**

```bash
cd demos/01-ir-runbooks
docarchive index docs --out runbooks.index.json
docarchive search runbooks.index.json "ransomware containment backups"
docarchive search runbooks.index.json "phishing" --tag identity
```

You can also run the CLI without installing, from the repo root:
`PYTHONPATH=src python -m docarchive index demos/01-ir-runbooks/docs --out /tmp/idx.json`

**How to act.** The first result of the ransomware query is the ransomware
containment runbook (top-ranked by score); open it and follow the containment
steps. The tag-filtered query returns only the phishing runbook, which carries
the `identity` tag.
