from gi.repository import GObject   #noqa

from models.plugin_mode import PluginMode

class PluginState(GObject.Object):
    __gsignals__ = {    # noqa: RUF012
        "plugin-changed": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str,),
        ),
    }

    def __init__(self):
        super().__init__()
        self.plugins = list(PluginMode)
        self.current = PluginMode.APPLICATIONS

    def set_plugin(self, plugin):
        if plugin == self.current:
            return

        self.current = plugin
        self.emit("plugin-changed", plugin)

    def get_plugin(self):
        return self.current

    def next_plugin(self):
        index = self.plugins.index(self.current)
        index = (index + 1) % len(self.plugins)
        self.set_plugin(self.plugins[index])

    def previous_plugin(self):
        index = self.plugins.index(self.current)
        index = (index - 1) % len(self.plugins)
        self.set_plugin(self.plugins[index])
