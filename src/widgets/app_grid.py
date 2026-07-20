from gi.repository import Gtk, Gio

from models.app_object import AppObject
from widgets.app_card import AppCard


class AppGrid(Gtk.ScrolledWindow):

    def __init__(self):
        super().__init__()

        self.store = Gio.ListStore()

        self.selection = Gtk.NoSelection(
            model=self.store
        )

        self.factory = Gtk.SignalListItemFactory()

        self.factory.connect(
            "setup",
            self.on_setup,
        )

        self.factory.connect(
            "bind",
            self.on_bind,
        )

        self.grid = Gtk.GridView(
            model=self.selection,
            factory=self.factory,
        )

        self.set_child(self.grid)

    def on_setup(self, factory, list_item):

        card = AppCard()

        list_item.set_child(card)

    def on_bind(self, factory, list_item):

        obj = list_item.get_item()

        card = list_item.get_child()

        card.set_app(obj.app)

    def set_apps(self, apps):

        self.store.remove_all()

        for app in apps:

            self.store.append(
                AppObject(app)
            )
