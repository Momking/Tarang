from gi.repository import Gtk   #noqa


class ApplicationHeader(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.set_size_request(100, 50)

        self.entry = Gtk.SearchEntry()
        self.entry.set_hexpand(True)
        self.entry.set_placeholder_text(
            "Search applications..."
        )
        self.add_css_class("search-bar")

        self.append(self.entry)
