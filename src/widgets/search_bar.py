from gi.repository import Gtk, Gdk, GObject


class SearchBar(Gtk.SearchEntry):

    __gsignals__ = {
        "move-next": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (),
        ),
        "move-previous": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (),
        ),
    }

    def __init__(self):
        super().__init__()

        self.set_placeholder_text(
            "Search applications..."
        )

        self.set_hexpand(True)

        self.set_margin_top(20)
        self.set_margin_start(20)
        self.set_margin_end(20)

        key_controller = Gtk.EventControllerKey.new()
        key_controller.connect("key-pressed", self.on_key_pressed)
        self.add_controller(key_controller)

    def on_key_pressed(self, controller, keyval, keycode, state):

        if keyval == Gdk.KEY_Down or keyval == Gdk.KEY_Right:
            self.emit("move-next")
            return True

        if keyval == Gdk.KEY_Up or keyval == Gdk.KEY_Left:
            self.emit("move-previous")
            return True

        return False
