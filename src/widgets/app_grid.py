from gi.repository import Gio

from models.app_object import AppObject


class AppGrid(Gtk.GridView):

    def __init__(self):

        super().__init__()
        store = Gio.ListStore.new(AppObject)
