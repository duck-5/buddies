from dataclasses import dataclass

@dataclass
class Event:
    time: str
    notification: bool
    importance: int
    description: str
