import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")
gi.require_version("GnomeDesktop", "4.0")

from controllers.plugin_docker_controller import PluginDockController   #noqa

from gi.repository import (
    Gtk,
    Gtk4LayerShell,
)
from pathlib import Path

from widgets.launcher_window import LauncherWindow
from services.theme_service import ThemeService
from models.plugin_state import PluginState
from widgets.docker_window import DockWindow


class LauncherApplication(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="dev.tarang.Launcher"
        )

    def do_activate(self):

        self.plugin_state = PluginState()

        self.launcher = LauncherWindow(
            self,
            self.plugin_state,
        )

        self.dock = DockWindow(
            self,
            self.plugin_state,
        )

        self.plugin_dock_controller = PluginDockController(
            self.dock.plugin_dock,
            self.plugin_state,
        )

        self.dock.present()
        self.launcher.present()

        theme = ThemeService()

        resources = Path(__file__).parent / "resources"

        theme.load(
            resources / "base.css",
            resources / "generated.css",
        )


if __name__ == "__main__":
    LauncherApplication().run()
