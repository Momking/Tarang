from dataclasses import dataclass

from models.app_info import AppInfo


@dataclass(slots=True)
class SearchResult:

    title: str

    subtitle: str

    icon: object | None

    data: object
