import threading    #noqa
from gi.repository import GLib

from models.plugin_mode import PluginMode


class SearchController:

    SEARCH_DELAY_MS = 50

    def __init__(
        self,
        plugin_manager,
        grid,
    ):
        self.plugins = plugin_manager
        self.grid = grid

        self.search_generation = 0
        self.pending_search = None

    def initialize(self):
        self.search("", PluginMode.APPLICATIONS)

    def start_search(self, query, plugin_mode):

        self.pending_search = None

        self.search_generation += 1

        generation = self.search_generation

        threading.Thread(
            target=self.search_worker,
            args=(query, plugin_mode, generation),
            daemon=True,
        ).start()

        return False

    def search(self, query, plugin_mode):

        if self.pending_search is not None:
            GLib.source_remove(self.pending_search)

        self.pending_search = GLib.timeout_add(
            self.SEARCH_DELAY_MS,
            self.start_search,
            query,
            plugin_mode,
        )

    def finish_search(
        self,
        generation,
        results,
    ):

        if generation != self.search_generation:
            return False

        self.grid.set_results(results)

        return False

    def search_worker(
        self,
        query,
        plugin_mode,
        generation,
    ):

        results = self.plugins.search(query, plugin_mode)

        GLib.idle_add(
            self.finish_search,
            generation,
            results,
        )

    def activate(self, result):

        self.plugins.activate(result)

    def activate_selected(self):

        self.grid.activate_selected()

    def move_next(self):
            self.grid.move_next()

    def move_previous(self):
        self.grid.move_previous()
