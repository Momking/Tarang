# models/clipboard_item.py

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class ClipboardItem:
    text: str
    timestamp: datetime
