from gi.repository import Gtk   #noqa


class FileFooter(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.set_size_request(100, 50)
