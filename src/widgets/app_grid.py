from gi.repository import Gtk, GObject, Gio, Gdk

from widgets.app_card import AppCard
from models.plugin_result_item import PluginResultItem
from models.view_mode import ViewMode


class AppGrid(Gtk.ScrolledWindow):

    __gsignals__ = {
            "app-activated": (
                GObject.SignalFlags.RUN_FIRST,
                None,
                (object,),
            ),
            "focus-panel": (
                GObject.SignalFlags.RUN_FIRST,
                None,
                (),
            ),
        }

    def __init__(self, plugin_mode):
        super().__init__()

        self.set_vexpand(True)
        self.set_hexpand(True)

        #--------------------------------------------------
        # Initialize the store and selection model

        self.store = Gio.ListStore.new(
            PluginResultItem
        )

        # print("store", self.store.get_n_items())

        self.selection = Gtk.SingleSelection(
            model=self.store
        )

        self.selection.connect(
            "selection-changed",
            self.on_selection_changed,
        )

        self.factory = Gtk.SignalListItemFactory()

        self.factory.connect("setup", self.on_setup)
        self.factory.connect("bind", self.on_bind)
        self.factory.connect("unbind", self.on_unbind)

        self.view_mode = plugin_mode

        self.rebuild_view(plugin_mode)

        key_controller = Gtk.EventControllerKey.new()
        key_controller.connect("key-pressed", self.on_key_pressed)
        self.add_controller(key_controller)

    def rebuild_view(self, mode: ViewMode):

        if hasattr(self, "grid"):
            self.grid.unparent()

        if mode == ViewMode.GRID:
            grid = Gtk.GridView(
                model=self.selection,
                factory=self.factory,
            )

            grid.set_min_columns(3)
            grid.set_max_columns(3)

        else:
            grid = Gtk.ListView(
                model=self.selection,
                factory=self.factory,
            )

        grid.connect(
            "activate",
            self.on_activate,
        )

        grid.set_enable_rubberband(False)
        grid.add_css_class("results")

        self.grid = grid
        self.set_child(grid)

        self.view_mode = mode

    def set_view_mode(self, mode):

        if mode == self.view_mode:
            return

        self.rebuild_view(mode)

    def set_results(self, results):

        self.store.remove_all()

        for result in results:
            self.store.append(
                PluginResultItem(result)
            )

        if self.store.get_n_items() > 0:
            self.selection.set_selected(0)

    def has_results(self):
        return self.store.get_n_items() > 0

    def on_setup(self, factory, list_item):
        card = AppCard()
        list_item.set_child(card)

        list_item.card = card

    def on_bind(self, factory, list_item):
        card = list_item.card

        plugin_result = list_item.get_item()
        card.set_result(plugin_result.result)

        if list_item.get_position() == self.selection.get_selected():
            card.add_css_class("selected")
        else:
            card.remove_css_class("selected")

        # Save the list item by position
        if not hasattr(self, "_list_items"):
            self._list_items = {}

        self._list_items[list_item.get_position()] = list_item

    def on_unbind(self, factory, list_item):
        self._list_items.pop(list_item.get_position(), None)
        card = list_item.get_child()

        card.set_result(None)

    def get_selected_item(self):

        return self.selection.get_selected_item()

    def get_selected_result(self):

        plugin_result = self.get_selected_item()

        if plugin_result is None:
            return None

        return plugin_result.result

    def activate_selected(self):

        result = self.get_selected_result()

        if result is None:
            return

        self.emit(
            "app-activated",
            result,
        )

    def on_activate(self, grid, position):
        print("ACTIVATE", position)

        item = self.store.get_item(position)

        self.emit(
            "app-activated",
            item.result,
        )

    def focus_grid(self):
        self.grid.grab_focus()

    def unfocus(self):
        self.get_root().set_focus(None)

    def move_next(self):

        index = self.selection.get_selected()

        if index == Gtk.INVALID_LIST_POSITION:
            return

        count = self.store.get_n_items()

        if index < count - 1:
            self.selection.set_selected(index + 1)
            self.grid.scroll_to(
                index + 1,
                Gtk.ListScrollFlags.SELECT,
                None,
            )

    def move_previous(self):

        index = self.selection.get_selected()

        if index == Gtk.INVALID_LIST_POSITION:
            return

        if index > 0:
            self.selection.set_selected(index - 1)
            self.grid.scroll_to(
                index - 1,
                Gtk.ListScrollFlags.SELECT,
                None,
            )

    def on_selection_changed(self, selection, position, n_items):
        selected = selection.get_selected()

        for pos, list_item in self._list_items.items():
            card = list_item.card

            if pos == selected:
                card.add_css_class("selected")
            else:
                card.remove_css_class("selected")

    def on_key_pressed(self, controller, keyval, keycode, state):
        print("app-grid: key pressed: ", Gdk.keyval_name(keyval))
        if keyval == Gdk.KEY_Tab:
            self.emit("focus-panel")
        return True
