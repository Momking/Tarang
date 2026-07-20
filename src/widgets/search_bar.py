from gi.repository import Gtk


class SearchBar(Gtk.SearchEntry):

    def __init__(self):
        super().__init__()

        self.set_placeholder_text(
            "Search applications..."
        )

        self.set_hexpand(True)

        self.set_margin_top(20)
        self.set_margin_start(20)
        self.set_margin_end(20)
