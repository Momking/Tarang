from gi.repository import GObject


class AppObject(GObject.Object):

    def __init__(self, app):

        super().__init__()

        self.app = app
