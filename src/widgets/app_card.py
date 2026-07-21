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

    def set_result(self, result):
        self.result = result
        print(result)

        self.label.set_text(result.result.title)

        if result.result.icon is not None:
            self.image.set_from_gicon(result.result.icon)

    def on_clicked(self, button):

        if self.result is None:
            return

        self.emit("activated")

    def set_selected(
        self,
        selected,
    ):
        if selected:
            self.add_css_class("selected")
        else:
            self.remove_css_class("selected")
