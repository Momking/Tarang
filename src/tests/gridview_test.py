import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, Gio, GObject


# -----------------------------
# Model
# -----------------------------

class Item(GObject.Object):

    def __init__(self, text):
        super().__init__()
        self.text = text


# -----------------------------
# Card
# -----------------------------

class Card(Gtk.Button):

    def __init__(self):
        super().__init__()

        self.set_has_frame(False)

        self.add_css_class("app-card")

        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8,
        )

        self.image = Gtk.Image(
            icon_name="firefox"
        )
        self.image.set_pixel_size(64)

        self.label = Gtk.Label(
            justify=Gtk.Justification.CENTER,
            wrap=True,
        )

        box.append(self.image)
        box.append(self.label)

        self.set_child(box)

    def bind(self, item):

        self.label.set_text(item.text)


# -----------------------------
# Window
# -----------------------------

class Window(Gtk.ApplicationWindow):

    def __init__(self, app):
        super().__init__(application=app)

        self.set_default_size(900, 600)

        #
        # Model
        #

        store = Gio.ListStore.new(Item)

        for i in range(50):
            store.append(
                Item(f"Application {i}")
            )

        selection = Gtk.SingleSelection(
            model=store
        )

        #
        # Factory
        #

        factory = Gtk.SignalListItemFactory()

        factory.connect(
            "setup",
            self.setup,
        )

        factory.connect(
            "bind",
            self.bind,
        )

        #
        # Grid
        #

        grid = Gtk.GridView(
            model=selection,
            factory=factory,
        )

        grid.set_enable_rubberband(False)

        grid.set_max_columns(6)

        grid.set_min_columns(3)

        scroll = Gtk.ScrolledWindow()

        scroll.set_child(grid)

        self.set_child(scroll)

    def setup(
        self,
        factory,
        list_item,
    ):

        list_item.set_child(
            Card()
        )

    def bind(
        self,
        factory,
        list_item,
    ):

        card = list_item.get_child()

        item = list_item.get_item()

        card.bind(item)


# -----------------------------
# Application
# -----------------------------

class App(Gtk.Application):

    def __init__(self):
        super().__init__()

    def do_activate(self):

        win = Window(self)

        win.present()


app = App()

app.run()
