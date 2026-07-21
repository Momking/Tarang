class SearchController:

    def __init__(
        self,
        plugin_manager,
        grid,
    ):

        self.plugins = plugin_manager

        self.grid = grid
