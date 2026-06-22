# Demo 08 - Security governance minutes, filtered by date

**Where the data came from.** A security steering committee archives its minutes
as markdown and JSON across quarters: Q4 2025, Q1 2026, and a Q2 2026 draft. All
are synthetic governance records.

**What to expect.** A governance analyst preparing a quarterly review wants only
recent minutes. The `--since` filter keeps documents dated on or after a cutoff,
demonstrating date-based scoping over a time series.

**Run it.**

```bash
cd demos/08-board-minutes
docarchive index docs --out minutes.index.json
docarchive search minutes.index.json "zero trust segmentation" --since 2026-01-01
docarchive search minutes.index.json "multi-factor authentication"
```

**How to act.** The `--since 2026-01-01` query returns only the Q1 and Q2 2026
minutes (the Q4 2025 record is excluded by date), so you review only the current
year. Dropping the filter shows the MFA rollout discussed across both the Q4
2025 and Q1 2026 sessions.
