from gi.repository import Gtk, GObject

from services.highlight_service import HighlightService


class AppCard(Gtk.Button):

    def __init__(self):
        super().__init__()

        self.result = None

        # self.set_has_frame(False)

        self.box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8,
        )

        self.image = Gtk.Image()
        # self.image.set_pixel_size(64)

        self.label = Gtk.Label()
        self.label.set_wrap(True)
        self.label.set_justify(
            Gtk.Justification.CENTER
        )

        self.box.append(self.image)
        self.box.append(self.label)

        self.set_child(self.box)

        self.set_focusable(False)

        self.add_css_class("app-card")

        self.image.add_css_class("icon")

        self.label.add_css_class("title")

    def set_result(self, result):
        self.result = result

        # Widget is being recycled
        if result is None:

            self.label.set_text("")
            self.image.clear()

            return

        self.label.set_use_markup(True)

        self.label.set_markup(

            HighlightService.markup(
                result.search_result.title,
                result.search_result.query,
            )

        )

        # self.label.set_text(result.result.title)

        if result.search_result.icon is not None:
            self.image.set_from_gicon(result.search_result.icon)
