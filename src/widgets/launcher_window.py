from gi.repository import Gtk

from services.application_service import ApplicationService
from services.search_service import SearchService

from widgets.search_bar import SearchBar
from widgets.app_grid import AppGrid


class LauncherWindow(Gtk.ApplicationWindow):

    def __init__(self, application):
        super().__init__(application=application)

        self.set_title("Gremlin Launcher")
        self.set_default_size(900, 700)

        self.application_service = ApplicationService()
        self.search_service = SearchService()

        self.all_apps = self.application_service.load()

        self.search = SearchBar()
        self.grid = AppGrid()

        self.grid.set_apps(self.all_apps)

        layout = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
        )

        layout.append(self.search)
        layout.append(self.grid)

        self.set_child(layout)
