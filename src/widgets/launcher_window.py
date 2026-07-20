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


        self.search = SearchBar()
        self.grid = AppGrid()
        self.load_apps()

        layout = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
        )

        layout.append(self.search)
        layout.append(self.grid)

        self.set_child(layout)

        self.search.connect(
            "search-changed",
            self.on_search_changed,
        )

    def on_search_changed(self, entry):

        query = entry.get_text()

        results = self.search_service.search(
            query,
            self.all_apps,
        )

        self.grid.set_apps(results)

    def load_apps(self):
        self.all_apps = self.application_service.load()

        self.grid.set_apps(self.all_apps)
