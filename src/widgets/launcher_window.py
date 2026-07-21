from gi.repository import Gtk, GLib

from services.application_service import ApplicationService
from services.usage_service import UsageService

from plugins.manager import PluginManager

from widgets.search_bar import SearchBar
from widgets.app_grid import AppGrid
from wayland.layer_shell import setup as setup_layer_shell


class LauncherWindow(Gtk.ApplicationWindow):

    def __init__(self, application):
        super().__init__(application=application)

        # Configure window
        self.set_title("Tarang Launcher")
        # self.set_default_size(900, 700)
        self.set_decorated(False)

        # Initialise layer shell
        setup_layer_shell(self)

        # Create services
        self.usage_service = UsageService()
        self.application_service = ApplicationService()

        self.plugin_manager = PluginManager(
            self.application_service,
            self.usage_service,
        )

        # Create Widgets
        self.search = SearchBar()
        self.grid = AppGrid()

        self.grid.connect(
            "app-activated",
            self.on_app_activated,
        )

        # Connect signals
        self.search.connect(
            "search-changed",
            self.on_search_changed,
        )

        self.search.connect(
            "activate",
            self.on_activate,
        )

        results = self.plugin_manager.search("")

        self.grid.set_results(results)

        # Build layout
        outer = Gtk.Box()

        outer.set_hexpand(True)
        outer.set_vexpand(True)

        outer.set_halign(Gtk.Align.CENTER)
        outer.set_valign(Gtk.Align.START)
        # outer.set_homogeneous(True)

        # outer.set_margin_top(100)
        # outer.set_margin_bottom(40)
        # outer.set_margin_start(40)
        # outer.set_margin_end(40)

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

        GLib.idle_add(
            self.search.grab_focus
        )

    def on_search_changed(self, entry):

        query = entry.get_text()

        results = self.plugin_manager.search(query)

        self.grid.set_results(results)

    def on_activate(self, entry):

        child = self.grid.activate_first()

        if child is None:
            return

        card = child.get_child()

        card.on_clicked(None)

    def on_app_activated(
        self,
        grid,
        result,
    ):
        self.plugin_manager.activate(result)

        self.close()
