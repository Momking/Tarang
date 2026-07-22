from dataclasses import dataclass


@dataclass(slots=True)
class ClipboardItem:
    text: str
    timestamp: float
