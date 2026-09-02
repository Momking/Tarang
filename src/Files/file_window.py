from pathlib import Path    #noqa

from gi.repository import Gtk

from wayland.layer_shell import setup_launcher as setup_layer_shell
from Files.file_scrollable_window import FileScrollableWindow
from Files.file_header import FileHeader
from Files.file_footer import FileFooter


class FileWindow(Gtk.Window):

    def __init__(self, is_initial=False):
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
        header = FileHeader()
        self.window.append(header)

        # Add a scrolled window
        scrolled_window = FileScrollableWindow()
        scrolled_window.set_vexpand(True)
        scrolled_window.set_hexpand(True)
        scrolled_window.set_valign(Gtk.Align.FILL)
        self.window.append(scrolled_window)

        # Footer
        footer = FileFooter()
        self.window.append(footer)
