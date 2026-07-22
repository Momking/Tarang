import sys
import json
from gi.repository import Gdk

class ClipboardService:

    MAX_HISTORY = 100

    CLIPBOARD_FILE = "~/.local/share/tarang/clipboard.json"
    
    def __init__(self):

        self.history = []

        display = Gdk.Display.get_default()

        clipboard = display.get_clipboard()

        self.start()

        clipboard.connect(
            "changed",
            self.on_changed,
        )

    def start(self):
        with open(self.CLIPBOARD_FILE, "r") as f:
            self.history = json.load(f)

    def copy(self, text):
        self.history.append(text)
        self.history = self.history[:self.MAX_HISTORY]

        with open(self.CLIPBOARD_FILE, "w") as f:
            json.dump(self.history, f)

    def search(self, query):

        query = query.lower()

        if not query:
            return []

        results = []

        for item in self.history:

            word = item.text.lower()

            if query not in word:
                continue

            score = self.score(
                query,
                item,
            )

            results.append(
                (
                    score,
                    item,
                )
            )

        results.sort(
            reverse=True,
            key=lambda item: item[0],
        )

        return [
            item
            for _, item in results[:self.MAX_HISTORY]
        ]

    @staticmethod
    def score(
        query,
        item,
    ):
        word = item.text.lower()

        if word == query:
            return sys.maxsize

        if word.startswith(query):
            return item.timestamp

        if query in word:
            return 500

        return 0

    def on_changed(self):
        pass
