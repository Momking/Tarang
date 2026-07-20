import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

from widgets.launcher_window import LauncherWindow


class LauncherApplication(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="dev.tarang.Launcher"
        )

    def do_activate(self):
        window = LauncherWindow(self)
        window.present()


if __name__ == "__main__":
    LauncherApplication().run()
