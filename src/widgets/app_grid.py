from gi.repository import Gtk, GObject

from widgets.app_card import AppCard


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

        self.flowbox = Gtk.FlowBox()

        self.flowbox.set_selection_mode(
            Gtk.SelectionMode.NONE
        )

        self.flowbox.set_max_children_per_line(6)
        self.flowbox.set_min_children_per_line(3)
        self.flowbox.set_row_spacing(16)
        self.flowbox.set_column_spacing(16)

        self.set_child(self.flowbox)

    def set_results(self, results):

        while (child := self.flowbox.get_first_child()) is not None:
            self.flowbox.remove(child)

        for result in results:
            card = AppCard()
            card.set_result(result)

            card.connect(
                "activated",
                self.on_card_activated,
            )

            self.flowbox.insert(card, -1)

    def on_card_activated(self, card):

        self.emit(
            "app-activated",
            card.result,
        )

    def activate_first(self):
        return self.flowbox.get_first_child()
