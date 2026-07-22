from plugins.builtin.application_plugin import ApplicationPlugin
from plugins.builtin.calculator_plugin import CalculatorPlugin
from plugins.builtin.file_plugin import FilePlugin


class PluginLoader:

    def load(
        self,
        application_service,
        usage_service,
        file_index_service,
    ):
        return [
            ApplicationPlugin(
                application_service,
                usage_service,
            ),
            CalculatorPlugin(),
            FilePlugin(
                file_index_service,
            ),
        ]
