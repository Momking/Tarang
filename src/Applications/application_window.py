from pathlib import Path    #noqa

from gi.repository import Gtk

from wayland.layer_shell import setup_launcher as setup_layer_shell
from Applications.application_scrollable_window import ApplicationScrollableWindow


class ApplicationWindow(Gtk.Window):

    def __init__(self):
        super().__init__()
        self.set_default_size(600, 400)

        setup_layer_shell(self)

        # Build layout
        self.window = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
        )

        self.set_child(self.window)

        # Header
        header = Gtk.Label(label="Header\n")
        self.window.append(header)

        # Add a scrolled window
        scrolled_window = ApplicationScrollableWindow()
        scrolled_window.set_vexpand(True)
        scrolled_window.set_hexpand(True) # Optional: ensures it fills left-to-right as well
        scrolled_window.set_valign(Gtk.Align.FILL)
        self.window.append(scrolled_window)

        # Footer
        footer = Gtk.Label(label="Footer")
        self.window.append(footer)
