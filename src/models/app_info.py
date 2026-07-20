from dataclasses import dataclass
from gi.repository import Gio


@dataclass(slots=True)
class AppInfo:
    app_info: Gio.DesktopAppInfo
    name: str
    executable: str
    icon: Gio.Icon | None
