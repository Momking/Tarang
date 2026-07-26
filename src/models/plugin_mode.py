from enum import StrEnum


class PluginMode(StrEnum):
    APPLICATIONS = "applications"
    FILES = "files"
    CLIPBOARD = "clipboard"
    COMMANDS = "commands"
    CALCULATOR = "calculator"
    EMOJI = "emoji"
