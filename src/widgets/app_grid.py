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

        self.selected_index = 0
        self.cards = []

    def set_results(self, results):

        self.clear()

        self.cards.clear()

        for result in results:

            card = AppCard()

            card.set_result(result)

            self.cards.append(card)

            card.connect(
                "activated",
                self.on_card_activated,
            )

            self.flowbox.insert(card, -1)

        self.selected_index = 0
        self.update_selection()

    def on_card_activated(self, card):

        self.emit(
            "app-activated",
            card.result,
        )

    def activate_selected(self):

        if not self.cards:
            return

        self.cards[
            self.selected_index
        ].on_clicked(None)

    def update_selection(self):

        for i, card in enumerate(self.cards):

            card.set_selected(
                i == self.selected_index
            )

    def move_next(self):

        if not self.cards:
            return

        self.selected_index = min(
            self.selected_index + 1,
            len(self.cards) - 1,
        )

        self.update_selection()

    def move_previous(self):

        if not self.cards:
            return

        self.selected_index = max(
            self.selected_index - 1,
            0,
        )

        self.update_selection()

    def clear(self):

        while (child := self.flowbox.get_first_child()) is not None:
            self.flowbox.remove(child)
