import gi

gi.require_version("Gtk4LayerShell", "1.0")

from gi.repository import Gtk4LayerShell


def setup(window):
    Gtk4LayerShell.init_for_window(window)

    Gtk4LayerShell.set_layer(
        window,
        Gtk4LayerShell.Layer.OVERLAY,
    )

    Gtk4LayerShell.set_keyboard_mode(
        window,
        Gtk4LayerShell.KeyboardMode.ON_DEMAND,
    )

    Gtk4LayerShell.set_anchor(
        window,
        Gtk4LayerShell.Edge.TOP,
        True,
    )

    Gtk4LayerShell.set_namespace(window, "tarang")
