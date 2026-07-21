from pathlib import Path
import json


class UsageService:

    def __init__(self):

        self.path = (
            Path.home()
            / ".local"
            / "share"
            / "tarang"
            / "usage.json"
        )

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if self.path.exists():
            self.data = json.loads(
                self.path.read_text()
            )
        else:
            self.data = {}
