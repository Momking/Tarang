from pathlib import Path
import json
import time

from models.usage_entry import UsageEntry


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

        self.data: dict[str, UsageEntry] = {}

        if self.path.exists():
            self.load()

    def load(self) -> None:

        raw = json.loads(self.path.read_text())

        self.data = {
            app_id: UsageEntry(**entry)
            for app_id, entry in raw.items()
        }

    def save(self) -> None:

        raw = {
            app_id: {
                "count": entry.count,
                "last_used": entry.last_used,
            }
            for app_id, entry in self.data.items()
        }

        self.path.write_text(
            json.dumps(
                raw,
                indent=4,
            )
        )

    def score(self, app_id: str) -> float:

        entry = self.data.get(app_id)

        if entry is None:
            return 0

        days = (
            time.time() - entry.last_used
        ) / 86400

        recency = 20 * (0.5 ** (days / 30))

        return entry.count + recency

    def launched(self, app_id: str) -> None:

        entry = self.data.get(app_id)

        if entry is None:
            entry = UsageEntry(
                count=0,
                last_used=0,
            )
            self.data[app_id] = entry

        entry.count += 1
        entry.last_used = time.time()

        self.save()
