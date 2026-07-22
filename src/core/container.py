class Container:

    def __init__(self):

        self._services = {}

    def register(
        self,
        key,
        service,
    ):

        self._services[key] = service

    def resolve(
        self,
        key,
    ):

        return self._services[key]
