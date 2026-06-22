---
title: OSINT Field Note - Lookalike Domain Monitoring
date: 2026-02-11
source: Cognis Digital Analyst Notebook
tags: osint, brand-protection, domains
---

# OSINT Field Note - Lookalike Domain Monitoring

Purpose: detect newly registered domains that impersonate the organization's
brand, which are commonly staged for phishing.

Method: query public certificate-transparency logs and a passive DNS source for
strings that are visual or typographic variants of the primary brand domain.
Record each candidate with its registration date and the source that surfaced
it. Separate observation from inference: a similar name is a lead, not proof of
intent.

Triage: prioritize candidates that resolve to live infrastructure and that host
a login form mirroring the brand. Escalate confirmed impersonations to takedown.
All collection uses publicly available information only.
