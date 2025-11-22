from dataclasses import dataclass

@dataclass
class Event:
    time: str
    notification: bool
    importance: int
    description: str
    has_passed: bool = False
