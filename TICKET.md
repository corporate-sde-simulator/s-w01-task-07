# SVC-1844: Fix SLA monitoring and escalation service

**Status:** In Progress · **Priority:** High
**Sprint:** Sprint 23 · **Story Points:** 5
**Reporter:** Vikrant Singh (Support Ops Lead) · **Assignee:** You (Intern)
**Due:** End of sprint (Friday)
**Labels:** ackend, python, support, sla
**Epic:** SVC-1820 (Support Operations Platform)
**Task Type:** Bug Fix

---

## Description

The SLA tracker is reporting wrong compliance rates and doesn't properly warn about approaching breaches. Manish wrote this before going on sabbatical. The bugs affect SLA compliance reporting and breach detection calculations.

## Requirements

- Track response and resolution SLAs per ticket priority
- Warn when tickets approach breach threshold (75%+ of SLA time used)
- Calculate compliance rate based on resolved tickets (not all tickets)
- Log escalations when SLA is breached

## Acceptance Criteria

- [ ] Bug #1 fixed: Breach warning uses strict `>` instead of `>=` (misses boundary)
- [ ] Bug #2 fixed: Compliance rate denominator uses total tickets instead of resolved tickets only
- [ ] All unit tests pass

## Design Notes

See `docs/DESIGN.md` for the SLA monitoring architecture.
See `.context/pr_comments.md` for Manish's design notes.
