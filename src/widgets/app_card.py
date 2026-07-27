from gi.repository import Gtk, GObject  # noqa

from services.highlight_service import HighlightService
from models.view_mode import ViewMode


class AppCard(Gtk.Box):

    def __init__(self, view_mode):
        super().__init__()

        self.result = None
        self.view_mode = view_mode

        # self.set_has_frame(False)

        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_spacing(8)

        self.image = Gtk.Image()
        # self.image.set_pixel_size(64)

        self.label = Gtk.Label()
        self.label.set_wrap(True)
        self.label.set_justify(
            Gtk.Justification.CENTER
        )

        self.append(self.image)
        self.append(self.label)

        self.set_focusable(False)

        self.add_css_class("app-card")

        self.image.add_css_class("icon")

        self.label.add_css_class("title")
        if self.view_mode == ViewMode.LIST:
            self.set_orientation(Gtk.Orientation.HORIZONTAL)
            self.label.set_xalign(0.0)
            self.label.set_hexpand(True)

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
        else:
            self.label.add_css_class("emoji")
