from dataclasses import dataclass
from typing import Callable

from gi.repository import Gio


@dataclass(slots=True)
class Command:

    name: str

    description: str

    icon: Gio.Icon

    callback: Callable[[], None]
