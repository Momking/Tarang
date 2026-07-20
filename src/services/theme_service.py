from pathlib import Path

from gi.repository import Gtk, Gio, GLib, Gdk


class ThemeService:

    def __init__(self):

        self.provider = Gtk.CssProvider()
        self.monitors = []
        self.reload_source = None

    def load(self, *files: Path):

        css = ""

        for file in files:
            css += file.read_text()
            css += "\n"

            monitor = Gio.File.new_for_path(
                str(file)
            ).monitor_file(
                Gio.FileMonitorFlags.NONE,
                None,
            )

            monitor.connect(
                "changed",
                self.on_css_changed,
            )

            self.monitors.append(
                monitor
            )

        self.files = files

        self.provider.load_from_string(css)

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            self.provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def on_css_changed(
        self,
        monitor,
        file,
        other_file,
        event,
    ):
        self.load(*self.files)
        if self.reload_source is not None:

            GLib.source_remove(
                self.reload_source
            )

        self.reload_source = GLib.timeout_add(
            100,
            self.reload,
        )

    def reload(self):

        css = ""

        for file in self.files:
            css += file.read_text()

        self.provider.load_from_string(css)
