from models.plugin_result import PluginResult   #noqa

from plugins.loader import PluginLoader


class PluginManager:

    def __init__(
        self,
        container,
    ):
        self.container = container
        loader = PluginLoader()

        self.plugins = loader.load(
            self.container,
        )

    def register(
        self,
        plugin,
    ):

        self.plugins.append(plugin)

    def search(self, query: str, plugin_mode: str, limit: int = 50) -> list[PluginResult]:
        results: list[PluginResult] = []

        for plugin in sorted(
            self.plugins,
            key=lambda p: p.priority,
            reverse=True,
        ):
            if plugin_mode and plugin.name != plugin_mode:
                continue
            plugin_results = plugin.search(query, limit)

            results.extend(
                PluginResult(
                    plugin=plugin,
                    search_result=result,
                )
                for result in plugin_results
            )

        return results

    def activate(
        self,
        result,
    ):

        plugin = result.plugin
        result = result.search_result

        plugin.activate(result)
