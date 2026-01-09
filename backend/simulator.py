import random
from datetime import datetime
from models import TrafficEvent

COUNTRIES = ["US", "DE", "FR", "NL", "RU", "CN"]
PROTOCOLS = ["HTTP", "HTTPS"]
ASNS = ["AS13335", "AS16509", "AS9009", "AS8075"]


def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))


def generate_traffic(attack=False, mitigated=False):
    if attack:
        base_rps = random.randint(3000, 8000)
        country = random.choice(["RU", "CN"])
    else:
        base_rps = random.randint(20, 120)
        country = random.choice(COUNTRIES)

    # DEFENCES REDUCE IMPACT
    if mitigated and attack:
        base_rps = int(base_rps * random.uniform(0.2, 0.4))

    return TrafficEvent(
        timestamp=datetime.utcnow(),
        source_ip=random_ip(),
        protocol=random.choice(PROTOCOLS),
        requests_per_second=base_rps,
        country=country,
        asn=random.choice(ASNS)
    )
