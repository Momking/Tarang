import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")
gi.require_version("GnomeDesktop", "4.0")

from gi.repository import (
    Gtk,
    Gtk4LayerShell,
    GLib
)
from pathlib import Path

from services.theme_service import ThemeService
from Applications.application_window import ApplicationWindow
from Files.file_window import FileWindow
from Emoji.emoji_window import EmojiWindow


class LauncherApplication(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="dev.tarang.Launcher"
        )
        self.window_list = []
        self.current_window = None
        self.animating = False  # Guard flag to prevent multi-swipe spamming

    def do_activate(self):
        self.app_window = ApplicationWindow()
        self.app_window.set_application(self)

        self.file_window = FileWindow()
        self.file_window.set_application(self)

        self.emoji_window = EmojiWindow()
        self.emoji_window.set_application(self)

        self.window_list = [self.app_window, self.file_window, self.emoji_window]

        # Register all windows so the app engine doesn't exit early
        for window in self.window_list:
            self.add_window(window)

        # Connect a single controller per window. The controller itself handles left vs right.
        for window in self.window_list:
            self.attach_swipe_trigger(window)

        # Present the starting dashboard window surface
        self.app_window.present()
        self.current_window = self.app_window

        theme = ThemeService()
        resources = Path(__file__).parent / "resources"
        theme.load(
            resources / "base.css",
            resources / "generated.css",
        )

    def slide_window_left(self, target_window):
        """Slides the new page in from the right edge toward the center."""
        if self.current_window == target_window or self.animating:
            return
        self.animating = True

        old_window = self.current_window
        self.current_window = target_window

        Gtk4LayerShell.set_margin(target_window, Gtk4LayerShell.Edge.LEFT, 1800)
        target_window.present()

        self.anim_step = 0
        self.total_steps = 25

        # We explicitly track starting positions and target positions to make the math simple
        old_start, old_end = 600, -800
        new_start, new_end = 1800, 600

        def animate_frame():
            self.anim_step += 1
            progress = self.anim_step / self.total_steps

            # Linear interpolation formula: start + (end - start) * progress
            old_margin = int(old_start + (old_end - old_start) * progress)
            new_margin = int(new_start + (new_end - new_start) * progress)

            Gtk4LayerShell.set_margin(old_window, Gtk4LayerShell.Edge.LEFT, old_margin)
            Gtk4LayerShell.set_margin(target_window, Gtk4LayerShell.Edge.LEFT, new_margin)

            if self.anim_step >= self.total_steps:
                old_window.hide()
                self.animating = False
                return False
            return True

        GLib.timeout_add(16, animate_frame)

    def slide_window_right(self, target_window):
        """Slides the previous page in from the left edge toward the center."""
        if self.current_window == target_window or self.animating:
            return
        self.animating = True

        old_window = self.current_window
        self.current_window = target_window

        target_window.present()
        Gtk4LayerShell.set_margin(target_window, Gtk4LayerShell.Edge.LEFT, -800)

        self.anim_step = 0
        self.total_steps = 25

        # Old window moves right: from 600 out to 1800
        old_start, old_end = 600, 1800
        # New window comes from left: from -800 into 600
        new_start, new_end = -800, 600

        def animate_frame():
            self.anim_step += 1
            progress = self.anim_step / self.total_steps

            old_margin = int(old_start + (old_end - old_start) * progress)
            new_margin = int(new_start + (new_end - new_start) * progress)

            Gtk4LayerShell.set_margin(old_window, Gtk4LayerShell.Edge.LEFT, old_margin)
            Gtk4LayerShell.set_margin(target_window, Gtk4LayerShell.Edge.LEFT, new_margin)

            if self.anim_step >= self.total_steps:
                old_window.hide()
                self.animating = False
                return False
            return True

        GLib.timeout_add(16, animate_frame)
        Gtk4LayerShell.set_margin(target_window, Gtk4LayerShell.Edge.LEFT, 600)


    def attach_swipe_trigger(self, source_window):
        root_child = source_window.get_child()
        if not root_child:
            return

        scroll_ctrl = Gtk.EventControllerScroll.new(
            Gtk.EventControllerScrollFlags.HORIZONTAL
        )
        scroll_ctrl.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)

        # We only need to pass the source_window context to determine neighbors dynamically
        scroll_ctrl.connect("scroll", self._on_trackpad_swipe, source_window)
        root_child.add_controller(scroll_ctrl)

    def _on_trackpad_swipe(self, controller, dx, dy, source_window):
        if self.animating or abs(dx) < 1.0: # Filter accidental drifts
            return False

        # Find where we are in our linear pipeline stack array
        current_idx = self.window_list.index(source_window)
        print(f"Current index: {current_idx}")

        # 1. SWIPE LEFT (Finger moves right-to-left): Move to NEXT window
        if dx > 5:
            if current_idx < len(self.window_list) - 1:
                target_window = self.window_list[current_idx + 1]
                print(f"Advancing Forward -> index {current_idx + 1}")
                self.slide_window_left(target_window)
                return True
            else:
                print("Boundary hit: No more windows to the right!")
                return False

        # 2. SWIPE RIGHT (Finger moves left-to-right): Return to PREVIOUS window
        elif dx < -5:
            if current_idx > 0:
                target_window = self.window_list[current_idx - 1]
                print(f"Returning Backward <- index {current_idx - 1}")
                self.slide_window_right(target_window)
                return True
            else:
                print("Boundary hit: Already at the first window!")
                return False

        return False

    def do_deactivate(self):
        self.app_window.destroy()
        self.file_window.destroy()
        self.emoji_window.destroy()

if __name__ == "__main__":
    LauncherApplication().run()
