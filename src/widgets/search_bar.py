from gi.repository import Gtk, Gdk, GObject


class SearchBar(Gtk.Box):

    __gsignals__ = {    # noqa: RUF012
        "close": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (),
        ),
        "search-changed": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (),
        ),
        "activate": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (),
        ),
        "next-plugin": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (),
        ),
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
        "focus-out": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (),
        ),
        "filter-changed": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str,),
        ),
    }

    def __init__(self):
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12,
        )

        self.add_css_class("search-bar")

        #
        # Search Entry
        #
        self.entry = Gtk.SearchEntry()
        self.entry.set_hexpand(True)
        self.entry.set_placeholder_text(
            "Search applications..."
        )

        self.entry.connect(
            "search-changed",
            lambda *_: self.emit("search-changed"),
        )

        self.entry.connect(
            "activate",
            lambda *_: self.emit("activate"),
        )

        key_controller = Gtk.EventControllerKey()
        key_controller.connect(
            "key-pressed",
            self.on_key_pressed,
        )

        self.entry.add_controller(key_controller)

        #
        # Filter DropDown
        #
        self.filters = Gtk.StringList()

        self.dropdown = Gtk.DropDown(
            model=self.filters,
        )

        self.dropdown.connect(
            "notify::selected",
            self.on_filter_changed,
        )

        self.dropdown.set_visible(True)
        self.filters.append("Applications")
        self.filters.append("Files")
        self.filters.append("Clipboard")
        self.filters.append("Emojis")
        self.filters.append("Calculator")
        self.filters.append("Commands")

        self.dropdown.add_css_class("dropdown")

        #
        # Layout
        #
        self.append(self.entry)
        self.append(self.dropdown)

    #
    # Public API
    #

    def get_text(self):
        return self.entry.get_text()

    def set_text(self, text):
        self.entry.set_text(text)

    def grab_focus(self):
        self.entry.grab_focus()

    def set_placeholder(self, text):
        self.entry.set_placeholder_text("Search " + text + "...")

    #
    # Filters
    #

    def set_filters(self, filters: list[str]):

        while self.filters.get_n_items():
            self.filters.remove(0)

        for item in filters:
            self.filters.append(item)

        self.dropdown.set_visible(bool(filters))

        if filters:
            self.dropdown.set_selected(0)

    def get_selected_filter(self):

        index = self.dropdown.get_selected()

        if index == Gtk.INVALID_LIST_POSITION:
            return None

        return self.filters.get_string(index)

    #
    # Signals
    #

    def on_filter_changed(self, *_):

        value = self.get_selected_filter()

        if value is not None:
            self.emit(
                "filter-changed",
                value,
            )

    def on_key_pressed(
        self,
        controller,
        keyval,
        keycode,
        state,
    ):

        ctrl = bool(state & Gdk.ModifierType.CONTROL_MASK)

        if ctrl and keyval == Gdk.KEY_Tab:
            self.emit("next-plugin")
            return True

        if keyval in (Gdk.KEY_Down, Gdk.KEY_Right):
            self.emit("move-next")
            return True

        if keyval in (Gdk.KEY_Up, Gdk.KEY_Left):
            self.emit("move-previous")
            return True

        if keyval == Gdk.KEY_Tab:
            self.emit("focus-out")
            return True

        if keyval == Gdk.KEY_Escape:
            self.emit("close")
            return True

        return False
