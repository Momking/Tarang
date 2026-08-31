from gi.repository import Gtk   #noqa

class ApplicationScrollableWindow(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()

        self.add_css_class("ScrollableWindow")
