from models import TrafficEvent, AttackAlert
from datetime import datetime

def analyze_event(event: TrafficEvent, mitigated: bool):
    if event.requests_per_second > 2000:
        return AttackAlert(
            timestamp=datetime.utcnow(),
            attack_type="HTTP Flood (L7)",
            severity="HIGH" if not mitigated else "MITIGATED",
            description=f"Excessive RPS from {event.source_ip}",
            mitigation_applied="Rate limiting + JS challenge"
            if mitigated else None
        )
    return None