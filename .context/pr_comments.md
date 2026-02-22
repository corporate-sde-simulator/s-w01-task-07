# PR Review - Ticket escalation workflow engine (by Vikram Singh)

## Reviewer: Pooja Reddy
---

**Overall:** Good foundation but critical bugs need fixing before merge.

### `escalationEngine.py`

> **Bug #1:** SLA breach time calculation does not exclude non-business hours and escalates during weekends
> This is the higher priority fix. Check the logic carefully and compare against the design doc.

### `slaTracker.py`

> **Bug #2:** Priority upgrade from P3 to P1 does not reset the SLA timer and uses original P3 SLA deadline
> This is more subtle but will cause issues in production. Make sure to add a test case for this.

---

**Vikram Singh**
> Acknowledged. I have documented the issues for whoever picks this up.
