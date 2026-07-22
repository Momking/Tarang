from gi.repository import Gio

import subprocess

from models.search_result import SearchResult
from plugins.plugin import Plugin
from models.command import Command



class CommandPlugin(Plugin):

    name = "command"

    description = "Search command"

    author = "Nishant"

    version = "1.0.0"

    priority = 100

    def __init__(self, container):
        self.commands = [
            Command(
                name="Shutdown",
                description="Power off the system",
                icon=Gio.ThemedIcon.new("system-shutdown"),
                callback=self.shutdown,
            ),
            Command(
                name="Reboot",
                description="Restart the system",
                icon=Gio.ThemedIcon.new("system-reboot"),
                callback=self.reboot,
            ),
            Command(
                name="Suspend",
                description="Suspend the system",
                icon=Gio.ThemedIcon.new("system-suspend"),
                callback=self.suspend,
            ),
            Command(
                name="Logout",
                description="Logout the system",
                icon=Gio.ThemedIcon.new("system-logout"),
                callback=self.logout,
            ),
            Command(
                name="Lock",
                description="Lock the system",
                icon=Gio.ThemedIcon.new("system-lock"),
                callback=self.lock,
            ),
        ]

    def search(self, query, limit):

        results = []

        for command in self.commands:
            score = self.score(query, command)

            if score == 0:
                continue

            results.append((score, command))

        results.sort(
            key=lambda x: x[0],
            reverse=True,
        )

        return [
            SearchResult(
                title=command.name,
                subtitle=command.description,
                icon=command.icon,
                data=command,
            )
            for _, command in results[:limit]
        ]

    @staticmethod
    def score(query: str, command: Command) -> int:

        query = query.lower()

        name = command.name.lower()

        if name == query:
            return 1000

        if name.startswith(query):
            return 800

        if query in name:
            return 500

        return 0

    def activate(self, result):

        command = result.data

        command.callback()

    def shutdown(self):
        subprocess.Popen(["systemctl", "poweroff"])

    def reboot(self):
        subprocess.Popen(["systemctl", "reboot"])

    def suspend(self):
        subprocess.Popen(["systemctl", "suspend"])

    def logout(self):
        pass

    def lock(self):
        pass
