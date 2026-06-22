---
title: Incident Response Runbook - Credential Phishing
date: 2026-02-03
source: SOC Playbook Library
tags: incident-response, phishing, identity
---

# Incident Response Runbook - Credential Phishing

This runbook covers the response to a reported credential-phishing campaign
targeting employee mailboxes. It assumes the responder has authorized access to
the mail gateway, identity provider, and endpoint logs for the affected tenant.

Triage:

- Confirm the reporting user and pull the original message headers from the mail
  gateway. Record the sending domain, return-path, and any redirect URLs.
- Search the gateway for other recipients of the same campaign by subject,
  sender, and URL pattern. Quarantine matching messages.

Containment:

- If credentials were entered, reset the affected account password and revoke
  active sessions and refresh tokens in the identity provider.
- Enable or verify multi-factor authentication on the account before re-enabling.

Eradication and recovery:

- Block the phishing domain at the gateway and at the resolver. Add the URL
  pattern to the detection ruleset.
- Review sign-in logs for the affected account over the prior seven days for
  anomalous geolocation or impossible-travel events.

Lessons learned should be filed within five business days. This document is
defensive guidance for authorized responders only.
