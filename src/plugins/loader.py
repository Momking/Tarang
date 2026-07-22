from plugins.builtin.application_plugin import ApplicationPlugin
from plugins.builtin.calculator_plugin import CalculatorPlugin
from plugins.builtin.file_plugin import FilePlugin
from plugins.builtin.clipboard_plugin import ClipboardPlugin

from plugins.plugin import Plugin
from plugins.plugin_settings import PluginSettings


class PluginLoader:

    def load(
        self,
        container,
    ):

        settings = PluginSettings().load()

        candidates = [
            ApplicationPlugin(
                container,
            ),
            CalculatorPlugin(
                container,
            ),
            FilePlugin(
                container,
            ),
            ClipboardPlugin(
                container,
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
