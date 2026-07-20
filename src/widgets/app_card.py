from gi.repository import Gtk


class AppCard(Gtk.Button):

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

        self.label.set_text(app.name)

        if app.icon is not None:
            self.image.set_from_gicon(app.icon)

    def on_clicked(self, button):

        if self.app is None:
            return

        self.app.app_info.launch(
            [],
            None,
        )
