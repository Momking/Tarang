from plugins.plugin import Plugin

from models.search_result import SearchResult
from services.application_service import ApplicationService
from services.usage_service import UsageService


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

        apps = self._cache

        if not query:
            matches = apps

        else:

            matches = [

                app

                for app in apps

                if query in app.name.casefold()

            ]

        matches.sort(
            key=lambda app: self.score(
                app,
                query,
            ),
            reverse=True,
        )

        return [

            SearchResult(

                title=app.name,

                subtitle=app.executable,

                icon=app.icon,

                data=app,

            )

            for app in matches[:limit]
        ]

    def score(
        self,
        app,
        query,
    ):

        score = 0

        name = app.name.casefold()

        if name.startswith(query):
            score += 100

        elif query in name:
            score += 50

        score += self.usage.score(
            app.app_info.get_id()
        )

        return score

    def activate(
        self,
        result: SearchResult,
    ):

        app = result.data

        app_id = app.app_info.get_id()

        self.usage.launched(app_id)

        app.app_info.launch([], None)
