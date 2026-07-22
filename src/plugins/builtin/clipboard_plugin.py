from gi.repository import Gio

from services.clipboard_service import ClipboardService
from models.search_result import SearchResult
from plugins.plugin import Plugin



class ClipboardPlugin(Plugin):

    name = "clipboard"

    description = "Search clipboard history"

    author = "Nishant"

    version = "1.0.0"

    priority = 100

    MAX_PREVIEW = 80

    def __init__(
        self,
        container,
    ):
        self.clipboard = container.resolve(
            ClipboardService,
        )

    def search(self, query, limit):

        items = self.clipboard.search(query)

        return [

            SearchResult(

                title = item.text.replace("\n", " ") 
                if len(item.text) > self.MAX_PREVIEW
                else item.text[:self.MAX_PREVIEW - 1] + "…",

                subtitle=str(item.timestamp),

                icon = Gio.ThemedIcon.new("clipboard"),

                data=item,

            )

            for item in items

        ]

    def activate(
        self,
        result,
    ):

        self.clipboard.copy(result.data.text)
