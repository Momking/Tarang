from gi.repository import Gtk, GLib, Gdk

from services.application_service import ApplicationService
from services.usage_service import UsageService
from services.clipboard_service import ClipboardService
from services.icon_cache import IconCache
from services.thumbnail_service import ThumbnailService
from widgets.panel import Panel

from controllers.search_controller import SearchController

from plugins.manager import PluginManager

from widgets.search_bar import SearchBar
from widgets.app_grid import AppGrid
from wayland.layer_shell import setup_launcher as setup_layer_shell

from services.file_index_service import FileIndexService
from core.container import Container
from models.mode import FocusMode
from models.view_mode import ViewMode
from models.plugin_mode import PluginMode


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

        self.view_mode = ViewMode.GRID

        self.mode = FocusMode.SEARCH

        self.plugin_mode = PluginMode.APPLICATIONS

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
        self.grid = AppGrid(self.view_mode)
        self.panel = Panel()

        self.controller = SearchController(
            self.plugin_manager,
            self.grid,
        )

        self.grid.connect(
            "app-activated",
            self.on_app_activated,
        )

        self.grid.connect(
            "focus-panel",
            lambda *_: self.panel.focus_panel(),
        )

        self.panel.connect(
            "focus-change",
            lambda *_: self.search.grab_focus(),
        )

        self.panel.connect(
            "plugin-mode-change",
            lambda _, mode: self.change_plugin_mode(mode),
        )

        # Connect signals
        self.search.connect(
            "search-changed",
            lambda entry: self.controller.search(
                entry.get_text(), self.plugin_mode
            ),
        )

        self.search.connect(
            "activate",
            lambda *_: self.controller.activate_selected(),
        )

        self.search.connect(
            "move-next",
            lambda *_: self.controller.move_next(),
        )

        self.search.connect(
            "move-previous",
            lambda *_: self.controller.move_previous(),
        )

        self.search.connect(
            "focus-out",
            lambda *_: self.focus_results(),
        )

        self.controller.initialize()

        # Build layout
        outer = Gtk.Box()

        outer.set_hexpand(True)
        outer.set_vexpand(True)

        content = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
        )

        content.add_css_class("launcher")

        content.append(self.search)
        content.append(self.grid)
        content.append(self.panel)

        outer.append(content)

        self.set_child(outer)

        # Search entry focus
        controller_search = Gtk.ShortcutController()

        shortcut = Gtk.Shortcut.new(
            Gtk.ShortcutTrigger.parse_string("Escape"),
            Gtk.CallbackAction.new(
                lambda *_: self.get_application().quit()
            ),
        )

        controller_search.add_shortcut(shortcut)

        self.search.add_controller(controller_search)

    def on_app_activated(
        self,
        grid,
        result,
    ):

        self.controller.activate(result)

        self.get_application().quit()

    def focus_results(self):

        if self.grid.has_results():
            self.grid.focus_grid()
        else:
            self.focus_panel()

    def focus_search(self):

        self.search.grab_focus()

    def focus_panel(self):

        self.panel.focus_panel()

    def change_plugin_mode(self, mode):
        self.plugin_mode = mode

        if self.plugin_mode == PluginMode.FILES or \
            self.plugin_mode == PluginMode.CLIPBOARD or \
            self.plugin_mode == PluginMode.COMMANDS:
            self.grid.set_view_mode(ViewMode.LIST)
        elif self.plugin_mode == PluginMode.APPLICATIONS or \
            self.plugin_mode == PluginMode.CALCULATOR or \
            self.plugin_mode == PluginMode.EMOJI:
            self.grid.set_view_mode(ViewMode.GRID)

        self.controller.search(
            self.search.get_text(),
            self.plugin_mode,
        )
        self.focus_search()
