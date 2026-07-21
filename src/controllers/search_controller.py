class SearchController:

    def __init__(
        self,
        plugin_manager,
        grid,
    ):
        self.plugins = plugin_manager
        self.grid = grid

    def initialize(self):
        self.search("")

    def search(self, query):

        results = self.plugins.search(query)

        self.grid.set_results(results)

    def activate(self, result):

        self.plugins.activate(result)

    def activate_selected(self):

        self.grid.activate_selected()

    def move_next(self):
            self.grid.move_next()
    
    def move_previous(self):
        self.grid.move_previous()
