from pathlib import Path

from gi.repository import Gtk


class ThemeService:

    def __init__(self):

        self.provider = Gtk.CssProvider()

    def load(self, css_path: Path):

        self.provider.load_from_path(str(css_path))

        Gtk.StyleContext.add_provider_for_display(
            Gtk.Display.get_default(),
            self.provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
