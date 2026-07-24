from gi.repository import GObject

from models.plugin_result import PluginResult


class PluginResultItem(GObject.Object):
    """
    Wrapper around PluginResult so it can be stored inside Gio.ListStore.
    """

    def __init__(self, result: PluginResult):
        super().__init__()

        self.result = result
