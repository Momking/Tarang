import json
from dataclasses import dataclass

from plugins.plugin import Plugin
from gi.repository import Gdk
from models.search_result import SearchResult

@dataclass(slots=True)
class Emoji:
    emoji: str
    name: str
    version: str
    status: str
    group: str
    subgroup: str

class EmojiPlugin(Plugin):

    name = "emoji"

    description = "Search for emojis"

    author = "Nishant"

    version = "1.0.0"

    priority = 200

    def __init__(
            self,
            container,
        ):

        with open("src/resources/emoji.json", encoding="utf-8") as f:
            data = json.load(f)

        self.emojis = [Emoji(**item) for item in data]

    def search(
        self,
        query,
        limit,
    ):
        query = query.strip()

        return [
            SearchResult(
                title=f"{emoji.emoji}",
                subtitle="Emoji",
                icon=None,
                data=emoji.emoji,
                query=query,
            )
            for emoji in self.emojis[:]
            if query in emoji.name.lower()
        ]

    def activate(
        self,
        result,
    ):

        value = result.data

        emoji = Gdk.Display.get_default().get_clipboard()

        emoji.set(value)
