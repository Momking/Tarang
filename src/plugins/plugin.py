from abc import ABC, abstractmethod


class Plugin(ABC):

    @abstractmethod
    def search(
        self,
        query,
        limit,
    ):
        ...

    @abstractmethod
    def activate(
        self,
        result,
    ):
        ...
