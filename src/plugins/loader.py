from plugins.builtin.application_plugin import ApplicationPlugin
from plugins.builtin.calculator_plugin import CalculatorPlugin
from plugins.builtin.file_plugin import FilePlugin
from plugins.plugin import Plugin
from plugins.plugin_settings import PluginSettings


class PluginLoader:

    def load(
        self,
        application_service,
        usage_service,
        file_index_service,
    ):

        settings = PluginSettings().load()

        candidates = [
            ApplicationPlugin(
                application_service,
                usage_service,
            ),
            CalculatorPlugin(),
            FilePlugin(
                file_index_service,
            ),
        ]

        return [
            self.validate(plugin)
            for plugin in candidates
            if settings.get(plugin.name, True)
        ]

    @staticmethod
    def validate(plugin):

        if not isinstance(plugin, Plugin):
            raise TypeError(
                f"{plugin} is not a Plugin"
            )

        return plugin
