from gi.repository import Gtk, GLib

from services.application_service import ApplicationService
from services.usage_service import UsageService
from services.clipboard_service import ClipboardService
from services.icon_cache import IconCache
from services.thumbnail_service import ThumbnailService


from controllers.search_controller import SearchController

from plugins.manager import PluginManager

from widgets.search_bar import SearchBar
from widgets.app_grid import AppGrid
from wayland.layer_shell import setup as setup_layer_shell

from services.file_index_service import FileIndexService
from core.container import Container


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
        self.container = Container()

        self.container.register(
            UsageService,
            UsageService(),
        )

        self.container.register(
            ApplicationService,
            ApplicationService(),
        )

        self.container.register(
            FileIndexService,
            FileIndexService(),
        )

        self.container.register(
            ClipboardService,
            ClipboardService(),
        )

        self.container.register(
            IconCache,
            IconCache(),
        )

        thumbnail_service = ThumbnailService()

        self.container.register(
            ThumbnailService,
            thumbnail_service,
        )

        self.plugin_manager = PluginManager(
            self.container,
        )

        # Create Widgets
        self.search = SearchBar()
        self.grid = AppGrid()

        self.controller = SearchController(
            self.plugin_manager,
            self.grid,
        )

        self.grid.connect(
            "app-activated",
            self.on_app_activated,
        )

        # Connect signals
        self.search.connect(
            "search-changed",
            lambda entry: self.controller.search(
                entry.get_text()
            ),
        )

        self.search.connect(
            "activate",
            lambda *_: self.controller.activate_selected(),
        )

        self.search.connect(
            "move-next",
            lambda *_:
                self.controller.move_next(),
        )

        self.search.connect(
            "move-previous",
            lambda *_:
                self.controller.move_previous(),
        )

        self.controller.initialize()

        # Build layout
        outer = Gtk.Box()

        outer.set_hexpand(True)
        outer.set_vexpand(True)

        outer.set_halign(Gtk.Align.CENTER)
        outer.set_valign(Gtk.Align.START)

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
                lambda *_: self.get_application().quit()
            ),
        )

        controller.add_shortcut(shortcut)

        self.search.add_controller(controller)

        GLib.idle_add(
            self.search.grab_focus
        )

    def on_app_activated(
        self,
        grid,
        result,
    ):

        self.controller.activate(result)

        self.get_application().quit()
