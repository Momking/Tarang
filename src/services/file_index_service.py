from pathlib import Path
import threading

from gi.repository import Gio


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

        self.monitors: dict[Path, Gio.FileMonitor] = {}

        self.setup_monitors()

        self.lock = threading.Lock()

        threading.Thread(

            target=self._build_index,

            daemon=True,

        ).start()

    def _build_index(self):

        new_files: list[FileInfo] = []

        for root in self.SEARCH_DIRS:

            if not root.exists():
                continue

            for path in root.rglob("*"):

                if any(part in self.IGNORE for part in path.parts):
                    continue

                if not path.is_file():
                    continue

                new_files.append(
                    FileInfo(
                        path=path,
                        name=path.name,
                    )
                )

        with self.lock:
            self.files = new_files

    def all_files(self):
        with self.lock:
            return self.files.copy()

    def setup_monitors(self):

        for directory in self.SEARCH_DIRS:

            if not directory.exists():
                continue

            for root in directory.rglob("*"):
                    if root.is_dir():
                        self.monitor_directory(root)

            self.monitor_directory(directory)

            monitor = (
                Gio.File.new_for_path(
                    str(directory)
                )
                .monitor_directory(
                    Gio.FileMonitorFlags.NONE,
                    None,
                )
            )

            monitor.connect(
                "changed",
                self.on_changed,
            )

            self.monitors[directory] = monitor

    def on_changed(
        self,
        monitor,
        file,
        other_file,
        event,
    ):
        path_str = file.get_path()

        if path_str is None:
            return

        path = Path(path_str)

        if event == Gio.FileMonitorEvent.CREATED:

            self.add_file(path)
        elif event == Gio.FileMonitorEvent.DELETED:

            self.remove_file(path)
        elif event == Gio.FileMonitorEvent.RENAMED:

            self.remove_file(path)

            if other_file:

                other_path = other_file.get_path()

                if other_path is not None:
                    self.add_file(Path(other_path))

    def add_file(
        self,
        path: Path,
    ):
        if path.is_dir():
            self.monitor_directory(path)
            return

        FileInfo(
            name=path.name,
            path=path,
        )


        if path.name.startswith("."):
            return

        if path.suffix in {

            ".swp",
            ".tmp",
            ".part",

        }:
            return

        with self.lock:
            if any(
                file.path == path
                for file in self.files
            ):
                return

            self.files.append(
                FileInfo(
                    name=path.name,
                    path=path,
                )
            )

    def remove_file(self, path: Path):

        if path.is_dir():
            self.unmonitor_directory(path)
            return

        with self.lock:
            self.files = [
                file
                for file in self.files
                if file.path != path
            ]

    def monitor_directory(self, directory: Path):

        if directory in self.monitors:
            return

        monitor = (
            Gio.File.new_for_path(str(directory))
            .monitor_directory(
                Gio.FileMonitorFlags.NONE,
                None,
            )
        )

        monitor.connect(
            "changed",
            self.on_changed,
        )

        self.monitors[directory] = monitor

    def unmonitor_directory(
        self,
        directory: Path,
    ):

        monitor = self.monitors.pop(
            directory,
            None,
        )

        if monitor:

            monitor.cancel()
