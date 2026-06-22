---
title: Coordinated Disclosure - Stored XSS in Comment Field
date: 2026-02-22
source: Cognis Digital AppSec Disclosures
tags: appsec, xss, web
---

# Coordinated Disclosure - Stored XSS in Comment Field

A stored cross-site scripting issue was reported in the comment field of a
support portal. User-supplied comment text was rendered into the agent console
without contextual output encoding, allowing script execution in the agent's
browser session.

Impact: an attacker comment could run script in the context of a support agent,
potentially exposing the agent's session.

Remediation: apply contextual HTML output encoding at render time and add a
content security policy that disallows inline script. A test now asserts that a
comment containing markup is rendered as inert text. This is an authorized
coordinated-disclosure record.
