from dataclasses import dataclass
from datetime import datetime

from models.clipboard_type import ClipboardType


@dataclass(slots=True)
class ClipboardEntry:
    type: ClipboardType

    preview: str

    mime_types: list[str]

    text: str | None = None

    image: bytes | None = None

    files: list[str] | None = None

    timestamp: datetime = datetime.now()
