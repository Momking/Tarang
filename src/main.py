import gi

from services.application_service import ApplicationService

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="dev.gremlin.Launcher"
        )

    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self)

        window.set_default_size(900, 700)

        window.present()


# Application().run()
service = ApplicationService()

apps = service.load()

assert len(apps) > 0

print(apps[0])
