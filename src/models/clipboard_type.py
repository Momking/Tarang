from enum import Enum


class ClipboardType(Enum):
    TEXT = "text"
    URL = "url"
    FILES = "files"
    IMAGE = "image"
    HTML = "html"
    COLOR = "color"
    CODE = "code"
    UNKNOWN = "unknown"
