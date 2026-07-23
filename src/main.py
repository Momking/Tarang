import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")
gi.require_version("GnomeDesktop", "4.0")

from gi.repository import (
    Gtk,
    Gtk4LayerShell,
)
from pathlib import Path

from widgets.launcher_window import LauncherWindow
from services.theme_service import ThemeService

class LauncherApplication(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="dev.tarang.Launcher"
        )

    def do_activate(self):
        window = LauncherWindow(self)
        window.present()

        theme = ThemeService()

        resources = Path(__file__).parent / "resources"

        theme.load(
            resources / "base.css",
            resources / "generated.css",
        )


if __name__ == "__main__":
    LauncherApplication().run()
