import re
from urllib.parse import urlparse

from models.clipboard_entry import ClipboardEntry
from models.clipboard_type import ClipboardType


class ClipboardParser:

    URL_RE = re.compile(r"^https?://")

    COLOR_RE = re.compile(
        r"^#(?:[0-9a-fA-F]{3}){1,2}$"
    )

    CODE_RE = re.compile(
        r"(class |def |import |#include|fn |public class)"
    )

    @staticmethod
    def parse_text(text: str) -> ClipboardEntry:

        text = text.strip()

        #
        # URL
        #

        parsed = urlparse(text)

        if parsed.scheme in ("http", "https") and parsed.netloc:
            return ClipboardEntry(
                type=ClipboardType.URL,
                preview=text,
                mime_types=["text/plain"],
                text=text,
            )

        #
        # Color
        #

        if ClipboardParser.COLOR_RE.match(text):
            return ClipboardEntry(
                type=ClipboardType.COLOR,
                preview=text,
                mime_types=["text/plain"],
                text=text,
            )

        #
        # Code
        #

        if ClipboardParser.CODE_RE.search(text):

            preview = text.splitlines()[0][:80]

            return ClipboardEntry(
                type=ClipboardType.CODE,
                preview=preview,
                mime_types=["text/plain"],
                text=text,
            )

        #
        # Plain Text
        #

        preview = text.replace("\n", " ")

        return ClipboardEntry(
            type=ClipboardType.TEXT,
            preview=preview[:80],
            mime_types=["text/plain"],
            text=text,
        )
