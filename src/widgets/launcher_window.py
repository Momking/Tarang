from gi.repository import Gtk

from services.application_service import ApplicationService
from widgets.app_grid import AppGrid


class LauncherWindow(Gtk.ApplicationWindow):

    def __init__(self, application):
        super().__init__(application=application)

        self.set_title("Gremlin Launcher")
        self.set_default_size(900, 700)

        self.application_service = ApplicationService()

        self.grid = AppGrid()

        self.set_child(self.grid)

        apps = self.application_service.load()

        self.grid.set_apps(apps)
