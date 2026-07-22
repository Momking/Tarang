import re
from plugins.plugin import Plugin
from gi.repository import Gdk
from models.search_result import SearchResult


PATTERN = re.compile(
    r"^[0-9+\-*/(). ]+$"
)

class CalculatorPlugin(Plugin):

    name = "calculator"

    priority = 200

    def search(
        self,
        query,
        limit,
    ):

        query = query.strip()

        if not PATTERN.fullmatch(query):
            return []

        try:
            result = str(
                eval(
                    query,
                    {},
                    {},
                )
            )
        except (SyntaxError, ZeroDivisionError, NameError):
            return []

        return [
            SearchResult(
                title=result,
                subtitle=query,
                icon=None,
                data=result,
            )
        ]

    def activate(
        self,
        result,
    ):

        value = result.data

        clipboard = Gdk.Display.get_default().get_clipboard()

        clipboard.set(value)
