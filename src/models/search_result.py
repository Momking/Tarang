from dataclasses import dataclass

from gi.repository import Gio


@dataclass(slots=True)
class SearchResult:

    title: str

    subtitle: str

    icon: Gio.Icon | None

    data: object
