from dataclasses import dataclass
from gi.repository import Gdk
from typing import TypeVar, Generic

T = TypeVar("T")

@dataclass(slots=True)
class SearchResult(Generic[T]):

    title: str

    subtitle: str

    icon: Gdk.Paintable | None

    data: T

    query: str

    score: int = 0
