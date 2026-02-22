"""
SLA Tracker — monitors service level agreements for support tickets.

Tracks response times, resolution times, and triggers escalation
when SLA breach thresholds approach.

Author: Manish Kapoor (on sabbatical)
Last Modified: 2026-01-18
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum


class Priority(Enum):
    CRITICAL = 'critical'  # 1h response, 4h resolution
    HIGH = 'high'         # 2h response, 8h resolution
    MEDIUM = 'medium'     # 4h response, 24h resolution
    LOW = 'low'           # 8h response, 48h resolution


SLA_TARGETS = {
    Priority.CRITICAL: {'response_hours': 1, 'resolution_hours': 4},
    Priority.HIGH: {'response_hours': 2, 'resolution_hours': 8},
    Priority.MEDIUM: {'response_hours': 4, 'resolution_hours': 24},
    Priority.LOW: {'response_hours': 8, 'resolution_hours': 48},
}


class SLATracker:
    def __init__(self, business_hours_start: int = 9, business_hours_end: int = 18):
        self.tickets: Dict[str, Dict] = {}
        self.business_start = business_hours_start
        self.business_end = business_hours_end
        self.escalation_log: List[Dict] = []

    def create_ticket(self, ticket_id: str, priority: Priority,
                      created_at: Optional[datetime] = None) -> Dict:
        """Create a new support ticket and start SLA clock."""
        if ticket_id in self.tickets:
            raise ValueError(f"Ticket {ticket_id} already exists")

        now = created_at or datetime.now()
        sla = SLA_TARGETS[priority]

        ticket = {
            'id': ticket_id,
            'priority': priority,
            'created_at': now,
            'responded_at': None,
            'resolved_at': None,
            'status': 'open',
            'response_deadline': now + timedelta(hours=sla['response_hours']),
            'resolution_deadline': now + timedelta(hours=sla['resolution_hours']),
            'escalation_level': 0,
            'sla_breached': False
        }

        self.tickets[ticket_id] = ticket
        return ticket

    def record_response(self, ticket_id: str,
                        responded_at: Optional[datetime] = None) -> Dict:
        """Record first response to a ticket."""
        ticket = self._get_ticket(ticket_id)
        now = responded_at or datetime.now()

        ticket['responded_at'] = now
        ticket['status'] = 'in_progress'

        # Check SLA compliance
        if now > ticket['response_deadline']:
            ticket['sla_breached'] = True
            self._log_escalation(ticket_id, 'response_sla_breached',
                                 f"Response took {self._hours_between(ticket['created_at'], now):.1f}h, target was {SLA_TARGETS[ticket['priority']]['response_hours']}h")

        return ticket

    def record_resolution(self, ticket_id: str,
                          resolved_at: Optional[datetime] = None) -> Dict:
        """Record ticket resolution."""
        ticket = self._get_ticket(ticket_id)
        now = resolved_at or datetime.now()

        ticket['resolved_at'] = now
        ticket['status'] = 'resolved'

        if now > ticket['resolution_deadline']:
            ticket['sla_breached'] = True
            self._log_escalation(ticket_id, 'resolution_sla_breached',
                                 f"Resolution took {self._hours_between(ticket['created_at'], now):.1f}h, target was {SLA_TARGETS[ticket['priority']]['resolution_hours']}h")

        return ticket

    def check_approaching_breach(self, warning_percent: float = 0.75) -> List[Dict]:
        """
        Find tickets approaching SLA breach.
        Returns tickets that have used more than warning_percent of their SLA time.
        """
        warnings = []
        now = datetime.now()

        for ticket_id, ticket in self.tickets.items():
            if ticket['status'] == 'resolved':
                continue

            # Check response SLA
            if not ticket['responded_at']:
                elapsed = self._hours_between(ticket['created_at'], now)
                target = SLA_TARGETS[ticket['priority']]['response_hours']
                # BUG: Uses elapsed > target * warning_percent
                # But should use elapsed >= target * warning_percent to catch exact boundary
                # Also, doesn't account for business hours — counts weekends/nights
                if elapsed > target * warning_percent:
                    warnings.append({
                        'ticket_id': ticket_id,
                        'type': 'response',
                        'elapsed_hours': round(elapsed, 2),
                        'target_hours': target,
                        'percent_used': round((elapsed / target) * 100, 1)
                    })

            # Check resolution SLA
            if ticket['status'] != 'resolved':
                elapsed = self._hours_between(ticket['created_at'], now)
                target = SLA_TARGETS[ticket['priority']]['resolution_hours']
                if elapsed > target * warning_percent:
                    warnings.append({
                        'ticket_id': ticket_id,
                        'type': 'resolution',
                        'elapsed_hours': round(elapsed, 2),
                        'target_hours': target,
                        'percent_used': round((elapsed / target) * 100, 1)
                    })

        return warnings

    def get_sla_report(self) -> Dict:
        """Generate SLA compliance report."""
        total = len(self.tickets)
        resolved = [t for t in self.tickets.values() if t['status'] == 'resolved']
        breached = [t for t in self.tickets.values() if t['sla_breached']]

        # BUG: Compliance rate denominator uses total tickets instead of resolved tickets
        # Unresolved tickets shouldn't count against compliance rate yet
        compliance_rate = ((total - len(breached)) / total * 100) if total > 0 else 100

        return {
            'total_tickets': total,
            'resolved': len(resolved),
            'open': total - len(resolved),
            'sla_breached': len(breached),
            'compliance_rate': round(compliance_rate, 1),
            'escalations': len(self.escalation_log)
        }

    def _get_ticket(self, ticket_id: str) -> Dict:
        ticket = self.tickets.get(ticket_id)
        if not ticket:
            raise ValueError(f"Ticket {ticket_id} not found")
        return ticket

    def _hours_between(self, start: datetime, end: datetime) -> float:
        delta = end - start
        return delta.total_seconds() / 3600

    def _log_escalation(self, ticket_id: str, reason: str, details: str):
        self.escalation_log.append({
            'ticket_id': ticket_id,
            'reason': reason,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
