import json
from pathlib import Path


class PluginSettings:

    CONFIG = (
        Path.home()
        / ".config"
        / "tarang"
        / "plugins.json"
    )

    def load(self):

        if not self.CONFIG.exists():
            return {}

        with self.CONFIG.open() as f:
            return json.load(f)
