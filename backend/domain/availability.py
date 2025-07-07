from dataclasses import dataclass

@dataclass
class Availability:
    date: str
    time: str
    courts_available: int