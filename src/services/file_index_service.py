import os
import json
import stat
import threading
from pathlib import Path

from gi.repository import Gio, GLib


from models.file_info import FileInfo


class FileIndexService:

    SEARCH_DIRS = (
        Path.home() / "Documents",
        Path.home() / "Downloads",
        Path.home() / "Projects",
    )

    CACHE_FILE = (
        Path.home()
        / ".cache"
        / "tarang"
        / "files.json"
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
        self._save_source = None

        self.files: list[FileInfo] = []

        self.monitors: dict[Path, Gio.FileMonitor] = {}

        self.setup_monitors()

        self.lock = threading.Lock()

        self.load_cache()

        threading.Thread(

            target=self.refresh_index,

            daemon=True,

        ).start()

    def iter_files(self):
        for root in self.SEARCH_DIRS:

            if not root.exists():
                continue

            for dirpath, dirnames, filenames in os.walk(root):

                # Prevent recursion into ignored directories
                dirnames[:] = [
                    d
                    for d in dirnames
                    if (
                        d not in self.IGNORE
                        and not d.startswith(".")
                    )
                ]

                for filename in filenames:

                    if filename.startswith("."):
                        continue

                    path = Path(dirpath) / filename

                    try:
                        mode = path.lstat().st_mode
                    except OSError:
                        continue

                    if not stat.S_ISREG(mode):
                        continue

                    yield path


    def refresh_index(self):

        new_files: list[FileInfo] = []

        for path in self.iter_files():
            new_files.append(
                FileInfo(
                    path=path,
                    name=path.name,
                )
            )

        # Keep deterministic ordering
        new_files.sort(key=lambda f: str(f.path))

        with self.lock:
            old_paths = {f.path for f in self.files}
            new_paths = {f.path for f in new_files}

            if len(new_files) != len(self.files):
                print(
                    "Different length:",
                    len(self.files),
                    len(new_files),
                )

            elif new_files != self.files:

                for old, new in zip(self.files, new_files):

                    if old != new:
                        print("First difference:")
                        print(old)
                        print(new)
                        break

            else:
                print("Index unchanged")
                return

            self.files = new_files

        missing = new_paths - old_paths
        extra = old_paths - new_paths

        print(f"Missing in cache: {len(missing)}")
        for p in sorted(missing):
            print(" +", p)

        print(f"Extra in cache: {len(extra)}")
        for p in sorted(extra):
            print(" -", p)

        self.schedule_save()

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

        self.schedule_save()

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

        self.schedule_save()

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

    def load_cache(self):

        if not self.CACHE_FILE.exists():
            return

        try:

            data = json.loads(
                self.CACHE_FILE.read_text()
            )

        except Exception:
            return

        with self.lock:

            self.files = [

                FileInfo.from_dict(item)

                for item in data

                if Path(item["path"]).exists()

            ]

    def save_cache(self):

        self.CACHE_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.lock:

            data = [
                file.to_dict()
                for file in self.files
            ]

        tmp = self.CACHE_FILE.with_suffix(".tmp")

        tmp.write_text(
            json.dumps(data)
        )

        tmp.replace(self.CACHE_FILE)

    def schedule_save(self):

        if self._save_source is not None:
            GLib.source_remove(self._save_source)

        self._save_source = GLib.timeout_add(
            1000,
            self._save_timeout,
        )

    def _save_timeout(self):

        self._save_source = None
        self.save_cache()

        return False
