class SearchService:
    def search(self, query: str, apps):
        query = query.casefold().strip()

        if not query:
            return apps

        return [
            app
            for app in apps
            if query in app.name.casefold()
        ]
