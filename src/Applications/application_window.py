from gi.repository import Gtk

class ApplicationWindow(Gtk.Window):

    def __init__(self):
        super().__init__()
        self.set_default_size(600, 400)


def on_activate(app):
    win = ApplicationWindow()
    win.set_application(app)
    win.present()


if __name__ == "__main__":
    app = Gtk.Application(application_id="com.example.CenteredScroll")
    app.connect('activate', on_activate)
    app.run(None)
