from html import escape


class HighlightService:

    @staticmethod
    def markup(
        text: str,
        query: str,
    ) -> str:

        if not query:
            return escape(text)

        lower = text.casefold()
        query = query.casefold()

        index = lower.find(query)

        if index == -1:
            return escape(text)

        end = index + len(query)

        return (
            escape(text[:index])
            + "<b>"
            + escape(text[index:end])
            + "</b>"
            + escape(text[end:])
        )