---
title: Coordinated Disclosure - IDOR in Reporting API
date: 2026-01-30
source: Cognis Digital AppSec Disclosures
tags: appsec, idor, authorization
---

# Coordinated Disclosure - IDOR in Reporting API

A researcher reported an insecure direct object reference in the reporting API
of an internally developed application. By incrementing a numeric report
identifier in the request path, an authenticated low-privilege user could
retrieve reports belonging to other tenants.

Impact: confidentiality. No integrity or availability impact was observed.

Root cause: the endpoint authenticated the caller but did not verify that the
caller was authorized for the requested object.

Remediation: enforce per-object authorization on every reporting endpoint and
add a regression test that a user cannot read another tenant's report. Fixed in
the 2026-02 release. This entry documents a coordinated, authorized disclosure.
