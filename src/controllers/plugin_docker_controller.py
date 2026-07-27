from gi.repository import Gdk, Gtk


class PluginDockController:

    def __init__(
        self,
        dock,
        plugin_state,
    ):
        self.dock = dock
        self.state = plugin_state

        self.plugins = list(dock.buttons.keys())

        self.selected = 0

        dock.connect(
            "plugin-clicked",
            self.on_plugin_clicked,
        )

        plugin_state.connect(
            "plugin-changed",
            self.on_plugin_changed,
        )

        key_controller = Gtk.EventControllerKey.new()
        key_controller.connect("key-pressed", self.on_key_pressed)
        self.dock.add_controller(key_controller)

    def on_key_pressed(self, key):
        if key == Gdk.KEY_Left:
            self.selected = (self.selected - 1) % len(self.plugins)
            self.update()
            return True

        if key == Gdk.KEY_Right:
            self.selected = (self.selected + 1) % len(self.plugins)
            self.update()
            return True

    def update(self):

        for button in self.dock.buttons.values():
            button.remove_css_class(
                "panel-window-button-active"
            )

        button = self.dock.buttons[
            self.plugins[self.selected]
        ]

        button.add_css_class(
            "panel-window-button-active"
        )

    def on_plugin_clicked(
        self,
        dock,
        mode,
    ):
        self.state.set_plugin(mode)

    def on_plugin_changed(
        self,
        state,
        mode,
    ):
        self.selected = self.plugins.index(mode)
        self.update()
