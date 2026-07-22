from dataclasses import dataclass


@dataclass(slots=True)
class UsageEntry:
    count: int
    last_used: float
