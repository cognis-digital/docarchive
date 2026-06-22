# Demo 04 - Public-records (FOIA-style) collection with stats

**Where the data came from.** A research team holds synthetic public-records
releases - a municipal IT budget summary, interagency coordination
correspondence, and a facility inspection report. All are clearly labelled
synthetic and contain no personal data or real jurisdictions.

**What to expect.** Before searching a freshly received records dump, an analyst
runs `stats` to understand its shape: how many documents, the date span, and the
tag distribution. Then a topic search surfaces the relevant record.

**Run it.**

```bash
cd demos/04-foia-records
docarchive index docs --out records.index.json
docarchive stats records.index.json
docarchive search records.index.json "cybersecurity budget logging"
```

**How to act.** `stats` shows the collection spans 2025-12-05 .. 2026-02-08 and
which tags dominate (`public-records` on all three, `government` on two). The
search then takes you to the budget summary, the record that discusses
cybersecurity tooling spend.
