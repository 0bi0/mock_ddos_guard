from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TrafficEvent(BaseModel):
    timestamp: datetime
    source_ip: str
    protocol: str
    requests_per_second: int
    country: str
    asn: str


class AttackAlert(BaseModel):
    timestamp: datetime
    attack_type: str
    severity: str
    description: str
    mitigation_applied: Optional[str] = None