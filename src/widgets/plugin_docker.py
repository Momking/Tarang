from gi.repository import Gtk, GObject  #noqa
from models.plugin_mode import PluginMode

class PluginDock(Gtk.Box):

    __gsignals__ = {    #noqa
        "plugin-clicked": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str,),
        ),
    }

    def __init__(self, plugin_state):
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8,
        )

        self.buttons = {}
        self.plugin_mode = plugin_state.get_plugin()


        plugins = [
            ("◼︎ Applications", PluginMode.APPLICATIONS),
            ("📁 Files", PluginMode.FILES),
            ("📋 Clipboard", PluginMode.CLIPBOARD),
            ("😊 Emoji", PluginMode.EMOJI),
            ("🧮 Calculator", PluginMode.CALCULATOR),
            ("⚙️ Commands", PluginMode.COMMANDS),
        ]

        for label, mode in plugins:
            button = Gtk.Button(label=label)

            button.set_hexpand(True)
            button.add_css_class("panel-window-button")

            button.connect(
                "clicked",
                lambda _, m=mode: self.emit(
                    "plugin-clicked",
                    m,
                ),
            )

            self.buttons[mode] = button
            self.append(button)

        self.add_css_class("panel-window")
