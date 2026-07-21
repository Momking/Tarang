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

    def search(
        self,
        query: str,
        limit: int = 20,
    ):

        results = []

        for plugin in self.plugins:

            plugin_results = plugin.search(query, limit)

            for result in plugin_results:
                results.append((plugin, result))

        return results

    def activate(
        self,
        item,
    ):

        plugin, result = item

        plugin.activate(result)
