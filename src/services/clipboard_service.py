from __future__ import annotations

import json
import time
from collections import deque
from pathlib import Path

from gi.repository import Gdk, GLib

from models.clipboard_item import ClipboardItem


class ClipboardService:

    MAX_HISTORY = 100

    SAVE_DELAY_MS = 1000

    MAX_TEXT_SIZE = 1024 * 1024  # 1 MiB

    CLIPBOARD_FILE = (
        Path.home()
        / ".local"
        / "share"
        / "tarang"
        / "clipboard.json"
    )

    def __init__(self):

        self.history = deque(maxlen=self.MAX_HISTORY)

        self._save_source = None

        self.display = Gdk.Display.get_default()
        self.clipboard = self.display.get_clipboard()

        self.ensure_storage()
        self.load()

        self.clipboard.connect(
            "changed",
            self.on_changed,
        )

    def ensure_storage(self) -> None:
            self.CLIPBOARD_FILE.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            if not self.CLIPBOARD_FILE.exists():
                self.CLIPBOARD_FILE.write_text("[]")

    def load(self):

        if not self.CLIPBOARD_FILE.exists():
            return

        try:
            with self.CLIPBOARD_FILE.open() as f:
                data = json.load(f)

        except json.JSONDecodeError:
            self.CLIPBOARD_FILE.write_text("[]")
            return

        except OSError:
            return

        for item in data:
            self.history.append(
                ClipboardItem(**item)
            )

    def save(self):

        self.CLIPBOARD_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.CLIPBOARD_FILE.open("w") as f:

            json.dump(
                [
                    {
                        "text": item.text,
                        "timestamp": item.timestamp,
                    }
                    for item in self.history
                ],
                f,
                indent=2,
            )

    def schedule_save(self):

        if self._save_source:

            GLib.source_remove(
                self._save_source
            )

        self._save_source = GLib.timeout_add(
            self.SAVE_DELAY_MS,
            self._save,
        )


    def _save(self):

        self.save()

        self._save_source = None

        return False

    def add_item(
        self,
        text: str,
    ):

        text = text.strip()

        if not text:
            return

        if len(text.encode("utf-8")) > self.MAX_TEXT_SIZE:
            return

        self.history = deque(
            (
                item
                for item in self.history
                if item.text != text
            ),
            maxlen=self.MAX_HISTORY,
        )

        self.history.appendleft(

            ClipboardItem(
                text=text,
                timestamp=time.time(),
            )

        )

        self.schedule_save()

    def copy(
        self,
        text: str,
    ):

        self.clipboard.set(text)

        self.add_item(text)

    def on_changed(
        self,
        clipboard,
    ):

        clipboard.read_text_async(
            None,
            self.on_text_received,
        )

    def on_text_received(
        self,
        clipboard,
        result,
    ):

        try:

            text = clipboard.read_text_finish(result)

        except Exception:

            return

        if text:

            self.add_item(text)

    def items(self):
        return self.history
