from gi.repository import Gio
import paperclip as pc

from services.clipboard_service import ClipboardService
from models.search_result import SearchResult
from plugins.plugin import Plugin



class ClipboardPlugin(Plugin):

    name = "clipboard"

    description = "Search clipboard history"

    author = "Nishant"

    version = "1.0.0"

    priority = 100

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

                title=item.text,

                subtitle=str(item.text),

                icon = Gio.File.new_for_path(
                    str(item.path)
                ).query_info(
                    "standard::icon",
                    Gio.FileQueryInfoFlags.NONE,
                    None,
                ).get_icon(),

                data=item,

            )

            for item in items

        ]

    def activate(
        self,
        result,
    ):

        file = result.data

        pc.copy(file.text)
