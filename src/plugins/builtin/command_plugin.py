from gi.repository import Gio

import subprocess

from models.search_result import SearchResult
from plugins.plugin import Plugin
from models.command import Command
from services.fuzzy_matcher import FuzzyMatcher



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
            match = FuzzyMatcher.match(
                query,
                command.name,
            )

            if not match.matched:
                continue

            results.append(
                (match.score, command)
            )

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
