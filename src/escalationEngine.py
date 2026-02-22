"""
Escalation Engine — manages ticket escalation workflows.

Escalates tickets through defined tiers when SLA thresholds
are breached or approaching breach.

Author: Manish Kapoor (on sabbatical)
Last Modified: 2026-01-18
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional


ESCALATION_TIERS = {
    0: {'label': 'Support Agent', 'auto_escalate_hours': 2},
    1: {'label': 'Team Lead', 'auto_escalate_hours': 4},
    2: {'label': 'Engineering Manager', 'auto_escalate_hours': 8},
    3: {'label': 'VP Engineering', 'auto_escalate_hours': None}  # Final tier
}


class EscalationEngine:
    def __init__(self):
        self.escalation_history: List[Dict] = []
        self.notification_queue: List[Dict] = []
        self.handlers: Dict[int, List[str]] = {
            0: [],  # Support agents
            1: [],  # Team leads
            2: [],  # Managers
            3: []   # VPs
        }

    def register_handler(self, tier: int, contact: str):
        """Register a person to receive escalation notifications for a tier."""
        if tier not in self.handlers:
            raise ValueError(f"Invalid tier: {tier}")
        if contact not in self.handlers[tier]:
            self.handlers[tier].append(contact)

    def escalate(self, ticket_id: str, current_tier: int,
                 reason: str) -> Dict:
        """
        Escalate a ticket to the next tier.
        Returns escalation details including who was notified.
        """
        next_tier = current_tier + 1

        if next_tier > max(ESCALATION_TIERS.keys()):
            return {
                'escalated': False,
                'reason': 'Already at maximum escalation tier',
                'tier': current_tier
            }

        tier_info = ESCALATION_TIERS[next_tier]
        handlers = self.handlers.get(next_tier, [])

        # Create escalation record
        record = {
            'ticket_id': ticket_id,
            'from_tier': current_tier,
            'to_tier': next_tier,
            'tier_label': tier_info['label'],
            'reason': reason,
            'notified': handlers,
            'timestamp': datetime.now().isoformat(),
            'acknowledged': False
        }

        self.escalation_history.append(record)

        # Queue notifications
        for handler in handlers:
            self.notification_queue.append({
                'to': handler,
                'ticket_id': ticket_id,
                'message': f"Ticket {ticket_id} escalated to {tier_info['label']}: {reason}",
                'priority': 'high' if next_tier >= 2 else 'normal',
                'sent': False
            })

        return {
            'escalated': True,
            'to_tier': next_tier,
            'tier_label': tier_info['label'],
            'handlers_notified': len(handlers)
        }

    def acknowledge_escalation(self, ticket_id: str, handler: str) -> bool:
        """Mark an escalation as acknowledged by a handler."""
        for record in reversed(self.escalation_history):
            if record['ticket_id'] == ticket_id and not record['acknowledged']:
                record['acknowledged'] = True
                record['acknowledged_by'] = handler
                record['acknowledged_at'] = datetime.now().isoformat()
                return True
        return False

    def get_pending_notifications(self) -> List[Dict]:
        """Return unsent notifications."""
        return [n for n in self.notification_queue if not n['sent']]

    def mark_notification_sent(self, index: int):
        """Mark a notification as sent."""
        if 0 <= index < len(self.notification_queue):
            self.notification_queue[index]['sent'] = True

    def get_escalation_summary(self) -> Dict:
        """Return summary of all escalations."""
        total = len(self.escalation_history)
        acknowledged = sum(1 for e in self.escalation_history if e['acknowledged'])
        pending_notifications = len(self.get_pending_notifications())

        return {
            'total_escalations': total,
            'acknowledged': acknowledged,
            'unacknowledged': total - acknowledged,
            'pending_notifications': pending_notifications
        }
