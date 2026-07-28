from gi.repository import Gtk, GLib, Gdk    # noqa

from services.application_service import ApplicationService
from services.usage_service import UsageService
from services.clipboard_service import ClipboardService
from services.icon_cache import IconCache
from services.thumbnail_service import ThumbnailService

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

    def __init__(self, application, plugin_state):
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

        self.plugin_state = plugin_state

        self.plugin_mode = plugin_state.get_plugin()

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

        self.controller = SearchController(
            self.plugin_manager,
            self.grid,
        )

        plugin_state.connect(
            "plugin-changed",
            self.on_plugin_changed,
        )

        self.grid.connect(
            "app-activated",
            self.on_app_activated,
        )

        self.grid.connect(
            "focus-search",
            lambda *_: self.focus_search(),
        )

        self.grid.connect(
            "next-plugin",
            lambda *_: self.plugin_state.next_plugin(),
        )

        self.grid.connect(
            "close",
            lambda *_: self.get_application().quit(),
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
            "next-plugin",
            lambda *_: self.plugin_state.next_plugin(),
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

        self.search.connect(
            "close",
            lambda *_: self.get_application().quit(),
        )

        self.controller.initialize()

        # Build layout
        outer = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
        )

        #
        # Header
        #
        header = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
        )
        header.add_css_class("launcher-header")
        header.append(self.search)

        separator = Gtk.Separator(
            orientation=Gtk.Orientation.HORIZONTAL,
        )

        #
        # Body
        #
        body = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
        )
        body.add_css_class("launcher-body")

        body.append(self.grid)

        self.footer = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12,
        )

        self.label1 = Gtk.Label(label=self.plugin_mode.upper())
        self.label2 = Gtk.Label(label="Press Ctrl+Tab to change plugin")
        self.label1.add_css_class("launcher-footer-label1")
        self.label2.add_css_class("launcher-footer-label2")

        self.label1.set_hexpand(False)
        self.label2.set_hexpand(True)
        self.label2.set_halign(Gtk.Align.END)
        self.label2.set_xalign(1.0)

        self.footer.append(self.label1)
        self.footer.append(self.label2)

        self.footer.add_css_class("launcher-footer")
        # footer.append(self.panel)

        # body.append(footer)

        outer.append(header)
        outer.append(separator)
        outer.append(body)
        outer.append(separator)
        outer.append(self.footer)

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

    def focus_search(self):

        self.search.grab_focus()

    def on_plugin_changed(self, plugin_state, mode):
        self.plugin_mode = mode
        self.change_footer(mode.upper())
        self.search.set_placeholder(plugin_state.get_plugin())

        if self.plugin_mode == PluginMode.FILES or \
            self.plugin_mode == PluginMode.CLIPBOARD:
            self.grid.set_view_mode(ViewMode.LIST)
        elif self.plugin_mode == PluginMode.APPLICATIONS or \
            self.plugin_mode == PluginMode.CALCULATOR or \
            self.plugin_mode == PluginMode.COMMANDS or \
            self.plugin_mode == PluginMode.EMOJI:
            self.grid.set_view_mode(ViewMode.GRID)

        self.controller.search(
            self.search.get_text(),
            self.plugin_mode,
        )
        self.focus_search()

    def change_footer(self, mode):
        self.label1.set_text(mode)
