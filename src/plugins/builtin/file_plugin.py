from gi.repository import Gio

from plugins.plugin import Plugin

from models.search_result import SearchResult
from services.file_index_service import FileIndexService
from services.fuzzy_matcher import FuzzyMatcher
from services.icon_cache import IconCache


class FilePlugin(Plugin):

    name = "files"

    description = "Search local files"

    author = "Nishant"

    version = "1.0.0"

    priority = 150

    def __init__(
        self,
        container,
    ):
        self.index = container.resolve(
            FileIndexService,
        )

        self.icons = container.resolve(
            IconCache,
        )


    def search(self, query, limit):

        matches = []

        for file in self.index.all_files():

            match = FuzzyMatcher.match(
                query,
                file.name,
            )

            if not match.matched:
                continue

            matches.append(
                (match.score, file)
            )

        matches.sort(
            key=lambda x: x[0],
            reverse=True,
        )

        return [

            SearchResult(

                title=file.name,

                subtitle=str(file.path),

                icon=self.icons.file_icon(
                    file.path,
                ),

                data=file,

            )

            for _, file in matches[:limit]

        ]

    def activate(
        self,
        result,
    ):

        file = result.data

        Gio.AppInfo.launch_default_for_uri(
            file.path.as_uri(),
            None,
        )
