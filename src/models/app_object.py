from gi.repository import GObject

from models.app_info import AppInfo


class AppObject(GObject.Object):

    def __init__(self, app: AppInfo):
        super().__init__()

        self.app = app
