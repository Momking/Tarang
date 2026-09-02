from pathlib import Path    #noqa

from gi.repository import Gtk

from wayland.layer_shell import setup_launcher as setup_layer_shell
from Applications.application_scrollable_window import ApplicationScrollableWindow
from Applications.application_header import ApplicationHeader
from Applications.application_footer import ApplicationFooter


class ApplicationWindow(Gtk.Window):

    def __init__(self, is_initial=True):
        super().__init__()
        # self.set_default_size(400, 600)

        starting_margin = 600 if is_initial else 1800
        setup_layer_shell(self, starting_left_margin=starting_margin)

        # Build layout
        self.window = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
        )

        self.set_child(self.window)
        self.add_css_class("app-window")

        # Header
        header = ApplicationHeader()
        self.window.append(header)

        # Add a scrolled window
        scrolled_window = ApplicationScrollableWindow()
        scrolled_window.set_vexpand(True)
        scrolled_window.set_hexpand(True)
        scrolled_window.set_valign(Gtk.Align.FILL)
        self.window.append(scrolled_window)

        # Footer
        footer = ApplicationFooter()
        self.window.append(footer)
