from gi.repository import Gtk

from services.application_service import ApplicationService
from services.search_service import SearchService

from widgets.search_bar import SearchBar
from widgets.app_grid import AppGrid
from wayland.layer_shell import setup as setup_layer_shell


class LauncherWindow(Gtk.ApplicationWindow):

    def __init__(self, application):
        super().__init__(application=application)

        # Configure window
        self.set_title("Tarang Launcher")
        self.set_default_size(900, 700)
        self.set_decorated(False)

        # Initialise layer shell
        setup_layer_shell(self)

        # Create services
        self.application_service = ApplicationService()
        self.search_service = SearchService()

        # Create Widgets
        self.search = SearchBar()
        self.grid = AppGrid()

        # Connect signals
        self.search.connect(
            "search-changed",
            self.on_search_changed,
        )

        self.search.connect(
            "activate",
            self.on_activate,
        )

        #Load applications
        self.load_apps()

        # Build layout
        outer = Gtk.Box()

        outer.set_hexpand(True)
        outer.set_vexpand(True)

        outer.set_halign(Gtk.Align.CENTER)
        outer.set_valign(Gtk.Align.START)

        outer.set_margin_top(60)
        outer.set_margin_bottom(40)
        outer.set_margin_start(40)
        outer.set_margin_end(40)

        content = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
        )

        content.add_css_class("launcher")

        content.set_size_request(900, 700)

        content.append(self.search)
        content.append(self.grid)

        outer.append(content)

        self.set_child(outer)

        # Search entry focus
        controller = Gtk.ShortcutController()

        shortcut = Gtk.Shortcut.new(
            Gtk.ShortcutTrigger.parse_string("Escape"),
            Gtk.CallbackAction.new(
                lambda *_: self.close()
            ),
        )

        controller.add_shortcut(shortcut)

        self.search.add_controller(controller)

        self.search.grab_focus()

    def on_search_changed(self, entry):

        query = entry.get_text()

        results = self.search_service.search(
            query,
            self.all_apps,
        )

        self.grid.set_apps(results)

    def on_activate(self, entry):

        child = self.grid.flowbox.get_first_child()

        if child is None:
            return

        card = child.get_child()

        card.on_clicked(None)

    def load_apps(self):
        self.all_apps = self.application_service.load()

        self.grid.set_apps(self.all_apps)
