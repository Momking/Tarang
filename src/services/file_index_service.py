from pathlib import Path
import threading

from models.file_info import FileInfo


class FileIndexService:

    SEARCH_DIRS = (
        Path.home() / "Documents",
        Path.home() / "Downloads",
        Path.home() / "Projects",
    )

    IGNORE = {
        ".git",
        "__pycache__",
        ".cache",
        "node_modules",
        "target",
        ".venv",
    }

    def __init__(self):
        self.files: list[FileInfo] = []

        threading.Thread(

            target=self._build_index,

            daemon=True,

        ).start()

    def _build_index(self):

        self.files.clear()

        for root in self.SEARCH_DIRS:

            if not root.exists():
                continue

            for path in root.rglob("*"):

                if any(
                    part in self.IGNORE
                    for part in path.parts
                ):
                    continue

                if not path.is_file():
                    continue

                self.files.append(

                    FileInfo(
                        path=path,
                        name=path.name,
                    )

                )

    def all_files(self):
        return self.files

    @staticmethod
    def score(
        query,
        name,
    ):

        if name == query:
            return 1000

        if name.startswith(query):
            return 800

        if query in name:
            return 500

        return 0
