from abc import ABC, abstractmethod

from models.search_result import SearchResult


class Plugin(ABC):

    name: str = ""
    description: str = ""
    enabled: bool = True
    version = "1.0.0"
    author = ""
    priority = 100

    @abstractmethod
    def search(
        self,
        query: str,
        limit: int,
    ) -> list[SearchResult]:
        ...

    @abstractmethod
    def activate(
        self,
        result: SearchResult,
    ) -> None:
        ...
