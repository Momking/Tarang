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

    def score(self, app_id):

        return self.data.get(
            app_id,
            0,
        )

    def launched(self, app_id):

        self.data[app_id] = (
            self.data.get(app_id, 0)
            + 1
        )

        self.path.write_text(
            json.dumps(
                self.data,
                indent=4,
            )
        )
