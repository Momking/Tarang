from enum import StrEnum


class PluginMode(StrEnum):
    APPLICATIONS = "applications"
    FILES = "files"
    CLIPBOARD = "clipboard"
    EMOJI = "emoji"
    CALCULATOR = "calculator"
    COMMANDS = "commands"
