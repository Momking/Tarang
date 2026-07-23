from dataclasses import dataclass
from gi.repository import Gdk


@dataclass(slots=True)
class SearchResult:

    title: str

    subtitle: str

    paintable: Gdk.Paintable | None

    data: object

    query: str
