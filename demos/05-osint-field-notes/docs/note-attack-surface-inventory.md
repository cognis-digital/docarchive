---
title: OSINT Field Note - External Attack Surface Inventory
date: 2026-03-04
source: Cognis Digital Analyst Notebook
tags: osint, attack-surface, asset-management
---

# OSINT Field Note - External Attack Surface Inventory

Purpose: maintain an accurate inventory of internet-facing assets the
organization owns, so that nothing is exposed without an owner and a reason.

Method: enumerate registered domains and subdomains from public sources,
correlate to owned network ranges, and record each live service with its
purpose. Flag assets that no owning team will claim as candidates for
decommissioning.

Cadence: refresh monthly and after any major deployment. The goal is reducing
unknown exposure. Collection relies solely on public records and the
organization's own authoritative asset data.
