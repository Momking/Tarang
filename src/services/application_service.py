from pathlib import Path
from gi.repository import Gio

from models.app_info import AppInfo

class ApplicationService:

    SEARCH_PATHS = (
        Path("/usr/share/applications"),
        Path.home() / ".local/share/applications",
    )

    def load(self):
        apps = []

        for directory in self.SEARCH_PATHS:

            if not directory.exists():
                continue

            for file in directory.glob("*.desktop"):
                try:
                    desktop = Gio.DesktopAppInfo.new_from_filename(str(file))
                except TypeError:
                    print(f"Skipping invalid desktop file: {file}")
                    continue

                if desktop is None:
                    continue

                if not desktop.should_show():
                    continue

                apps.append(

                    AppInfo(

                        app_info=desktop,

                        name=desktop.get_display_name(),

                        executable=desktop.get_executable(),

                        icon=desktop.get_icon(),

                    )

                )

        apps.sort(
            key=lambda app: app.name.casefold()
        )

        return apps
