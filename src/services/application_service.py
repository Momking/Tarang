from pathlib import Path


class ApplicationService:

    SEARCH_PATHS = (
        Path("/usr/share/applications"),
        Path.home() / ".local/share/applications",
    )

    def load(self):
        pass
