class SearchService:
    def __init__(self, usage_service):
        self.usage = usage_service

    def search(self, query: str, apps):
        self.query = query.casefold().strip()

        if not self.query:
            return apps

        filtered_apps = [
            app
            for app in apps
            if self.query in app.name.casefold()
        ]

        return sorted(
            filtered_apps,
            key=lambda app: self.score(app, self.query),
            reverse=True,
        )

    def score(self, app, query):

        name = app.name.casefold()

        score = 0

        if name.startswith(query):
            score += 100

        elif query in name:
            score += 50

        score += self.usage.score(
            app.app_info.get_id()
        )

        return score
