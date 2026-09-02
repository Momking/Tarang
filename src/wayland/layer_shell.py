import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")

from gi.repository import Gtk4LayerShell   #noqa

def get_window_size(window):
    display = window.get_display()
    monitor = display.get_monitors().get_item(0)
    geometry = monitor.get_geometry()
    return geometry.width, geometry.height

def setup_launcher(window, starting_left_margin):
    Gtk4LayerShell.init_for_window(window)

    Gtk4LayerShell.set_layer(
        window,
        Gtk4LayerShell.Layer.OVERLAY,
    )

    Gtk4LayerShell.set_keyboard_mode(
        window,
        Gtk4LayerShell.KeyboardMode.ON_DEMAND,
    )

    window_width, window_height = get_window_size(window)
    window.set_default_size(600, 600)
    # left = (geometry.width - window_width) // 2
    # top = (geometry.height - window_height) // 2
    # window.set_default_size(window_width/2, window_height/1.5)

    Gtk4LayerShell.set_anchor(window, Gtk4LayerShell.Edge.TOP, True)
    Gtk4LayerShell.set_anchor(window, Gtk4LayerShell.Edge.LEFT, True)
    Gtk4LayerShell.set_anchor(window, Gtk4LayerShell.Edge.BOTTOM, False)
    Gtk4LayerShell.set_anchor(window, Gtk4LayerShell.Edge.RIGHT, False)

    # Y-Axis placement
    Gtk4LayerShell.set_margin(window, Gtk4LayerShell.Edge.TOP, window_height // 4)

    # X-Axis placement managed dynamically by the slide controller
    print(f"starting_left_margin: {starting_left_margin}")
    Gtk4LayerShell.set_margin(window, Gtk4LayerShell.Edge.LEFT, starting_left_margin)

    Gtk4LayerShell.set_namespace(window, "tarang-launcher")

def setup_docker(window):
    Gtk4LayerShell.init_for_window(window)

    Gtk4LayerShell.set_layer(
        window,
        Gtk4LayerShell.Layer.OVERLAY,
    )

    Gtk4LayerShell.set_keyboard_mode(
        window,
        Gtk4LayerShell.KeyboardMode.ON_DEMAND,
    )

    # window_width, window_height = get_window_size(window)
    # window.set_default_size(window_width/2, window_height/8)

    Gtk4LayerShell.set_anchor(window, Gtk4LayerShell.Edge.TOP, False)
    Gtk4LayerShell.set_anchor(window, Gtk4LayerShell.Edge.LEFT, False)
    Gtk4LayerShell.set_anchor(window, Gtk4LayerShell.Edge.BOTTOM, True)
    Gtk4LayerShell.set_anchor(window, Gtk4LayerShell.Edge.RIGHT, False)

    Gtk4LayerShell.set_margin(window, Gtk4LayerShell.Edge.BOTTOM, 100)

    Gtk4LayerShell.set_namespace(window, "tarang-launcher")
