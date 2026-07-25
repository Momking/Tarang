from gi.repository import Gtk, Gdk, GObject


class Panel(Gtk.Box):
    __gsignals__ = {
        "focus-change": (GObject.SignalFlags.RUN_FIRST, None, ()),
    }

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        self.clipboard = Gtk.Button(label="Clipboard")
        self.emoji = Gtk.Button(label="Emoji")
        self.calc = Gtk.Button(label="Calculator")

        self.append(self.clipboard)
        self.append(self.emoji)
        self.append(self.calc)

        self.clipboard.set_hexpand(True)
        self.emoji.set_hexpand(True)
        self.calc.set_hexpand(True)

        key_controller = Gtk.EventControllerKey.new()
        key_controller.connect("key-pressed", self.on_key_pressed)
        self.add_controller(key_controller)

        self.add_css_class("panel-window")

    def on_key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Tab:
            self.emit("focus-change")
            return True
        return False

    def focus_panel(self):
        self.clipboard.grab_focus()
