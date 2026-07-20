import gi

gi.require_version("Gtk4LayerShell", "1.0")

from gi.repository import Gtk4LayerShell


def setup(window):
    Gtk4LayerShell.init_for_window(window)