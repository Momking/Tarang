from pathlib import Path

from gi.repository import Gio


class IconCache:

    def __init__(self):

        self._cache: dict[Path, Gio.Icon | None] = {}

    def file_icon(
        self,
        path: Path,
    ) -> Gio.Icon | None:

        icon = self._cache.get(path)

        if icon is not None:
            return icon

        try:

            icon = (
                Gio.File.new_for_path(str(path))
                .query_info(
                    "standard::icon",
                    Gio.FileQueryInfoFlags.NONE,
                    None,
                )
                .get_icon()
            )

        except Exception:
            icon = None

        self._cache[path] = icon

        return icon

    def themed(
        self,
        name: str,
    ):
    
        icon = self._cache.get(name)
    
        if icon is None:
    
            icon = Gio.ThemedIcon.new(name)
    
            self._cache[name] = icon
    
        return icon