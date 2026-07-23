from __future__ import annotations

import threading
from hashlib import md5
from pathlib import Path
from queue import Queue

from gi.repository import (
    Gdk,
    Gio,
    GLib,
    GObject,
    Gtk,
    GnomeDesktop,
)


class ThumbnailService(GObject.Object):

    __gsignals__ = {
        "thumbnail-ready": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str,),
        )
    }

    THUMBNAIL_DIR = (
        Path.home()
        / ".cache"
        / "thumbnails"
        / "normal"
    )

    def __init__(self):
        super().__init__()

        self.cache: dict[Path, Gdk.Paintable] = {}

        self.pending: set[Path] = set()

        self.queue: Queue[Path] = Queue()

        self.lock = threading.Lock()

        self.factory = (
            GnomeDesktop.DesktopThumbnailFactory.new(
                GnomeDesktop.DesktopThumbnailSize.NORMAL
            )
        )

        threading.Thread(
            target=self._worker,
            daemon=True,
        ).start()

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def get(
        self,
        path: Path,
    ) -> Gdk.Paintable | None:

        with self.lock:
            paintable = self.cache.get(path)

        if paintable is not None:
            return paintable

        texture = self._load_thumbnail(path)

        if texture is not None:

            with self.lock:
                self.cache[path] = texture

            return texture

        icon = self._fallback_icon(path)

        if icon is None:
            return None

        with self.lock:

            self.cache[path] = icon

            if path not in self.pending:

                self.pending.add(path)

                self.queue.put(path)

        return icon

    # -------------------------------------------------
    # Worker
    # -------------------------------------------------

    def _worker(self):

        while True:

            path = self.queue.get()

            try:
                self._generate_thumbnail(path)

            finally:

                with self.lock:
                    self.pending.discard(path)

                self.queue.task_done()

    # -------------------------------------------------
    # Thumbnail loading
    # -------------------------------------------------

    def _load_thumbnail(
        self,
        path: Path,
    ) -> Gdk.Texture | None:

        thumb = self.thumbnail_path(path)

        if not thumb.exists():
            return None

        try:

            return Gdk.Texture.new_from_filename(
                str(thumb)
            )

        except GLib.Error:

            return None

    # -------------------------------------------------
    # MIME icon
    # -------------------------------------------------

    def _fallback_icon(
        self,
        path: Path,
    ) -> Gdk.Paintable | None:

        try:

            file = Gio.File.new_for_path(str(path))

            info = file.query_info(
                "standard::icon",
                Gio.FileQueryInfoFlags.NONE,
                None,
            )

        except GLib.Error:

            return None

        display = Gdk.Display.get_default()

        if display is None:
            return None

        theme = Gtk.IconTheme.get_for_display(display)

        return theme.lookup_by_gicon(
            info.get_icon(),
            64,                      # desired size
            1,                       # scale
            Gtk.TextDirection.NONE,
            Gtk.IconLookupFlags.PRELOAD,
        )

    # -------------------------------------------------
    # Thumbnail generation
    # -------------------------------------------------

    def _generate_thumbnail(
        self,
        path: Path,
    ):

        try:

            file = Gio.File.new_for_path(str(path))

            info = file.query_info(
                "standard::content-type,time::modified",
                Gio.FileQueryInfoFlags.NONE,
                None,
            )

        except GLib.Error:

            return

        uri = file.get_uri()

        mime = info.get_content_type()

        mtime = info.get_attribute_uint64(
            "time::modified"
        )

        if not self.factory.can_thumbnail(
            uri,
            mime,
            mtime,
        ):
            return

        try:

            pixbuf = self.factory.generate_thumbnail(
                uri,
                mime,
            )

        except GLib.Error:

            return

        if pixbuf is None:
            return

        try:

            self.factory.save_thumbnail(
                pixbuf,
                uri,
                mtime,
            )

        except GLib.Error:

            return

        texture = self._load_thumbnail(path)

        if texture is None:
            return

        with self.lock:
            self.cache[path] = texture

        GLib.idle_add(
            self.emit,
            "thumbnail-ready",
            str(path),
        )

    # -------------------------------------------------
    # Thumbnail cache path
    # -------------------------------------------------

    def thumbnail_path(
        self,
        path: Path,
    ) -> Path:

        uri = path.resolve().as_uri()

        filename = (
            md5(uri.encode()).hexdigest()
            + ".png"
        )

        return self.THUMBNAIL_DIR / filename
