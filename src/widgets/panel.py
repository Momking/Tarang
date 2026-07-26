from gi.repository import Gtk, Gdk, GObject

from models.plugin_mode import PluginMode


class Panel(Gtk.Box):
    __gsignals__ = {
        "focus-change": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "plugin-mode-change": (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        self.applications = Gtk.Button(label="◼︎ Applications")
        self.files = Gtk.Button(label="📁 Files")
        self.clipboard = Gtk.Button(label="📋 Clipboard")
        self.emoji = Gtk.Button(label="😊 Emoji")
        self.calc = Gtk.Button(label="🧮 Calculator")

        self.applications.connect("clicked", self.on_applications_clicked)
        self.files.connect("clicked", self.on_files_clicked)
        self.clipboard.connect("clicked", self.on_clipboard_clicked)
        self.emoji.connect("clicked", self.on_emoji_clicked)
        self.calc.connect("clicked", self.on_calc_clicked)


        self.append(self.applications)
        self.append(self.files)
        self.append(self.clipboard)
        self.append(self.emoji)
        self.append(self.calc)

        self.applications.set_hexpand(True)
        self.files.set_hexpand(True)
        self.clipboard.set_hexpand(True)
        self.emoji.set_hexpand(True)
        self.calc.set_hexpand(True)

        key_controller = Gtk.EventControllerKey.new()
        key_controller.connect("key-pressed", self.on_key_pressed)
        self.add_controller(key_controller)

        self.add_css_class("panel-window")
        self.applications.add_css_class("panel-window-button")
        self.files.add_css_class("panel-window-button")
        self.clipboard.add_css_class("panel-window-button")
        self.emoji.add_css_class("panel-window-button")
        self.calc.add_css_class("panel-window-button")

        self.selected_index = 0
        self.plugin_list = [self.applications, self.files, self.clipboard, self.emoji, self.calc]


    def on_key_pressed(self, controller, keyval, keycode, state):
        print("panel: key pressed: ", Gdk.keyval_name(keyval))

        if keyval == Gdk.KEY_Left:
            self.plugin_list[self.selected_index].remove_css_class("panel-window-button-active")
            self.selected_index = (self.selected_index - 1) % 5
            self.focus_panel()
            return True

        if keyval == Gdk.KEY_Right:
            self.plugin_list[self.selected_index].remove_css_class("panel-window-button-active")
            self.selected_index = (self.selected_index + 1) % 5
            self.focus_panel()
            return True

        if keyval == Gdk.KEY_Tab:
            self.emit("focus-change")
            return True
        return False

    def focus_panel(self):
        self.plugin_list[self.selected_index].grab_focus()
        self.plugin_list[self.selected_index].add_css_class("panel-window-button-active")

    def on_applications_clicked(self, button):
        self.emit("plugin-mode-change", PluginMode.APPLICATIONS)

    def on_files_clicked(self, button):
        self.emit("plugin-mode-change", PluginMode.FILES)

    def on_clipboard_clicked(self, button):
        self.emit("plugin-mode-change", PluginMode.CLIPBOARD)

    def on_emoji_clicked(self, button):
        self.emit("plugin-mode-change", PluginMode.EMOJI)

    def on_calc_clicked(self, button):
        self.emit("plugin-mode-change", PluginMode.CALCULATOR)
