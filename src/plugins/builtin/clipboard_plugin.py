from gi.repository import Gio

from services.clipboard_service import ClipboardService
from models.search_result import SearchResult
from plugins.plugin import Plugin
from services.fuzzy_matcher import FuzzyMatcher
from services.icon_cache import IconCache


class ClipboardPlugin(Plugin):

    name = "clipboard"

    description = "Search clipboard history"

    author = "Nishant"

    version = "1.0.0"

    priority = 100

    MAX_PREVIEW = 20

    def __init__(
        self,
        container,
    ):
        self.clipboard = container.resolve(
            ClipboardService,
        )

        self.icons = container.resolve(
            IconCache,
        )


    def search(
        self,
        query,
        limit,
    ):

        matches = []

        for item in self.clipboard.items():

            match = FuzzyMatcher.match(
                query,
                item.text,
            )

            if not match.matched:
                continue

            matches.append(
                (match.score, item)
            )

        matches.sort(
            key=lambda x: x[0],
            reverse=True,
        )

        return [

            SearchResult(

                title=(
                    item.text[: self.MAX_PREVIEW]
                    if len(item.text) <= self.MAX_PREVIEW
                    else item.text[: self.MAX_PREVIEW - 1] + "…"
                ).replace("\n", " "),

                subtitle=str(item.timestamp),

                icon=self.icons.themed(
                    "edit-paste"
                ),

                data=item,
                query=query,
            )

            for _, item in matches[:limit]

        ]

    def activate(
        self,
        result,
    ):

        self.clipboard.copy(result.data.text)
