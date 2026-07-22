from models.plugin_result import PluginResult

from plugins.loader import PluginLoader


class PluginManager:

    def __init__(
        self,
        application_service,
        usage_service,
        file_index_service,
    ):
        loader = PluginLoader()

        self.plugins = loader.load(
            application_service,
            usage_service,
            file_index_service,
        )

    def register(
        self,
        plugin,
    ):

        self.plugins.append(plugin)

    def search(self, query: str, limit: int = 50) -> list[PluginResult]:
        results: list[PluginResult] = []

        for plugin in sorted(
            self.plugins,
            key=lambda p: p.priority,
            reverse=True,
        ):
            plugin_results = plugin.search(query, limit)

            results.extend(
                PluginResult(
                    plugin=plugin,
                    result=result,
                )
                for result in plugin_results
            )

        return results

    def activate(
        self,
        result,
    ):

        plugin = result.plugin
        result = result.result

        plugin.activate(result)
