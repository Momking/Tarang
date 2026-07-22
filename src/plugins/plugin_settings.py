from __future__ import annotations

import json
from pathlib import Path


class PluginSettings:

    CONFIG_FILE = (
        Path.home()
        / ".config"
        / "tarang"
        / "plugins.json"
    )

    DEFAULTS = {
        "applications": True,
        "calculator": True,
        "clipboard": True,
        "commands": True,
        "files": True,
    }

    def __init__(self) -> None:
        self._settings = self.load()

    def load(self) -> dict[str, bool]:
        self.CONFIG_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.CONFIG_FILE.exists():
            self.save(self.DEFAULTS)
            return self.DEFAULTS.copy()

        try:
            with self.CONFIG_FILE.open() as f:
                data = json.load(f)

        except Exception:
            self.save(self.DEFAULTS)
            return self.DEFAULTS.copy()

        settings = self.DEFAULTS.copy()
        settings.update(data)

        return settings

    def save(
        self,
        settings: dict[str, bool],
    ) -> None:

        with self.CONFIG_FILE.open("w") as f:
            json.dump(
                settings,
                f,
                indent=4,
            )

        self._settings = settings

    def enabled(
        self,
        plugin: str,
    ) -> bool:

        return self._settings.get(plugin, True)
