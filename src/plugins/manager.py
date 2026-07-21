from plugins.application import ApplicationPlugin

class PluginManager:

    def __init__(
        self,
        application_service,
        usage_service,
    ):
        self.plugins = []

        self.register(
            ApplicationPlugin(
                application_service,
                usage_service,
            )
        )

    def register(
        self,
        plugin,
    ):

        self.plugins.append(plugin)

    def search(self, query, limit=50):

        results = []

        for plugin in sorted(
            self.plugins,
            key=lambda p: p.priority,
            reverse=True,
        ):
            results.extend(plugin.search(query, limit))

        return results

    def activate(
        self,
        item,
    ):

        plugin, result = item

        plugin.activate(result)
