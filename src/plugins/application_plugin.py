from plugins.plugin import Plugin

from models.search_result import SearchResult


class ApplicationPlugin(Plugin):

    def __init__(
        self,
        application_service,
        search_service,
    ):

        self.apps = application_service

        self.search = search_service
