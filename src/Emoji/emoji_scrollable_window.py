from gi.repository import Gtk   #noqa

class EmojiScrollableWindow(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()

        self.add_css_class("ScrollableWindow")
