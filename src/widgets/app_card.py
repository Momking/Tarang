from gi.repository import Gtk


class AppCard(Gtk.Button):

    def __init__(self):
        super().__init__()

        self.set_has_frame(False)

        self.box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8,
        )

        self.image = Gtk.Image()

        self.label = Gtk.Label()

        self.box.append(self.image)
        self.box.append(self.label)

        self.set_child(self.box)
