---
title: Incident Response Runbook - Suspected Data Exfiltration
date: 2026-02-27
source: SOC Playbook Library
tags: incident-response, data-loss, network
---

# Incident Response Runbook - Suspected Data Exfiltration

This runbook addresses alerts suggesting unauthorized bulk data transfer out of
the environment, such as large outbound transfers to unfamiliar destinations.

Triage:

- Correlate the data-loss-prevention alert with proxy and firewall flow logs.
  Establish the source host, destination, volume, and time window.
- Identify the data classification of the source repository to gauge impact.

Containment:

- Block the destination at the egress proxy and firewall. Suspend the involved
  account pending review.
- Preserve flow records, proxy logs, and host artifacts under chain of custody.

Investigation:

- Reconstruct the timeline of access to the source repository. Distinguish
  routine business transfer from anomalous staging and compression activity.
- Assess whether the transfer used an approved channel or an unsanctioned one.

Document findings and notify the privacy and legal teams if regulated data is
implicated. For authorized internal investigations only.
