from pathlib import Path

from gi.repository import Gtk


class ThemeService:

    def __init__(self):

        self.provider = Gtk.CssProvider()

    def load(self, *files: Path):

        css = ""

        for file in files:
            css += file.read_text()
            css += "\n"

        self.provider.load_from_string(css)

        Gtk.StyleContext.add_provider_for_display(
            Gtk.Display.get_default(),
            self.provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
