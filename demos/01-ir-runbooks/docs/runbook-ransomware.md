---
title: Incident Response Runbook - Ransomware Containment
date: 2026-01-19
source: SOC Playbook Library
tags: incident-response, ransomware, containment
---

# Incident Response Runbook - Ransomware Containment

Authorized responders use this runbook when endpoint telemetry or user reports
indicate file encryption consistent with ransomware on managed hosts.

Immediate containment:

- Isolate affected hosts from the network using the endpoint agent's containment
  action; do not power them off, to preserve volatile memory for analysis.
- Disable the compromised service accounts and rotate any credentials they hold.

Scoping:

- Identify the initial access vector from authentication and process-creation
  logs. Determine lateral-movement paths and which file shares were reached.
- Verify the integrity and offline status of the most recent backups before any
  restoration attempt.

Recovery:

- Rebuild from known-good images rather than decrypting in place. Restore data
  from validated backups onto clean hosts.
- Stage a phased reconnection with heightened monitoring on restored segments.

Engage legal and communications per the organization's plan. This guidance is
strictly defensive and intended for incidents on systems you are authorized to
defend.
