from plugins.plugin import Plugin

from models.search_result import SearchResult
from services.application_service import ApplicationService
from services.usage_service import UsageService
from services.fuzzy_matcher import FuzzyMatcher


class ApplicationPlugin(Plugin):

    name = "applications"

    description = "Search installed desktop applications"

    author = "Nishant"

    version = "1.0.0"

    priority = 200

    def __init__(
        self,
        container,
    ):

        self.apps = container.resolve(
                    ApplicationService,
                )
        self.usage = container.resolve(
                    UsageService,
                )
        self._cache = self.apps.load()

    def search(
        self,
        query: str,
        limit: int,
    ) -> list[SearchResult]:

        query = query.casefold().strip()

        matches = []

        for app in self._cache:

            if query:
                match = FuzzyMatcher.match(query, app.name)

                if not match.matched:
                    continue

                score = match.score
            else:
                score = 0

            score += self.usage.score(
                app.app_info.get_id()
            )

            matches.append((app, score))

        matches.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return [
            SearchResult(
                title=app.name,
                subtitle=app.executable,
                icon=app.icon,
                data=app,
                query=query,
            )
            for app, _ in matches[:limit]
        ]

    def activate(
        self,
        result: SearchResult,
    ):

        app = result.data

        app_id = app.app_info.get_id()

        self.usage.launched(app_id)

        app.app_info.launch([], None)
