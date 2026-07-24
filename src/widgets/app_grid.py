from gi.repository import Gtk, GObject, Gio

from widgets.app_card import AppCard
from models.plugin_result_item import PluginResultItem


class AppGrid(Gtk.ScrolledWindow):

    __gsignals__ = {
            "app-activated": (
                GObject.SignalFlags.RUN_FIRST,
                None,
                (object,),
            ),
        }

    def __init__(self):
        super().__init__()

        self.set_vexpand(True)
        self.set_hexpand(True)

        #--------------------------------------------------
        # Initialize the store and selection model

        self.store = Gio.ListStore.new(
            PluginResultItem
        )

        self.selection = Gtk.SingleSelection(
            model=self.store
        )

        factory = Gtk.SignalListItemFactory()

        factory.connect(
            "setup",
            self.on_setup,
        )

        factory.connect(
            "bind",
            self.on_bind,
        )

        factory.connect(
            "unbind",
            self.on_unbind,
        )

        self.grid = Gtk.GridView(
            model=self.selection,
            factory=factory,
        )

        self.grid.set_enable_rubberband(False)

        self.grid.set_max_columns(6)
        self.grid.set_min_columns(3)

        self.set_child(self.grid)

    def set_results(self, results):

        self.result = results

        if results is None:
            self.label.set_text("")
            self.image.clear()
            return

        self.store.remove_all()

        for result in results:
            self.store.append(
                PluginResultItem(result)
            )

        if self.store.get_n_items() > 0:
            self.selection.set_selected(0)

    def on_setup(
        self,
        factory,
        list_item,
    ):

        card = AppCard()

        self.grid.connect(
            "activate",
            self.on_activate,
        )

        list_item.set_child(card)

    def on_bind(
        self,
        factory,
        list_item,
    ):

        card = list_item.get_child()

        plugin_result = list_item.get_item()

        card.set_result(
            plugin_result.result
        )

    def on_unbind(
        self,
        factory,
        list_item,
    ):
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

        item = self.store.get_item(position)

        self.emit(
            "app-activated",
            item.result,
        )

    def move_next(self):

        index = self.selection.get_selected()

        if index == Gtk.INVALID_LIST_POSITION:
            return

        count = self.store.get_n_items()

        if index < count - 1:
            self.selection.set_selected(index + 1)

    def move_previous(self):

        index = self.selection.get_selected()

        if index == Gtk.INVALID_LIST_POSITION:
            return

        if index > 0:
            self.selection.set_selected(index - 1)
