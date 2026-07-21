from gi.repository import Gtk, GObject


class AppCard(Gtk.Button):

    __gsignals__ = {
            "activated": (
                GObject.SignalFlags.RUN_FIRST,
                None,
                (),
            ),
        }

    def __init__(self):
        super().__init__()

        self.set_has_frame(False)

        self.add_css_class("app-card")

        self.box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8,
        )

        self.image = Gtk.Image()
        self.image.set_pixel_size(64)

        self.label = Gtk.Label()
        self.label.set_wrap(True)
        self.label.set_justify(
            Gtk.Justification.CENTER
        )

        self.box.append(self.image)
        self.box.append(self.label)

        self.connect(
            "clicked",
            self.on_clicked,
        )

        self.set_child(self.box)

    def set_app(self, app):
        self.app = app

        self.label.set_text(app[1].title)

        if app[1].icon is not None:
            self.image.set_from_gicon(app[1].icon)

    def on_clicked(self, button):

        if self.app is None:
            return

        self.emit("activated")
