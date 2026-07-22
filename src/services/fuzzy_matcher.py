from dataclasses import dataclass


@dataclass(slots=True)
class MatchResult:
    matched: bool
    score: int


class FuzzyMatcher:

    @staticmethod
    def match(query: str, text: str) -> MatchResult:
        query = query.lower().strip()
        text = text.lower()

        if not query:
            return MatchResult(True, 0)

        if text == query:
            return MatchResult(True, 1000)

        if text.startswith(query):
            return MatchResult(True, 800)

        if query in text:
            return MatchResult(True, 500)

        return MatchResult(False, 0)
