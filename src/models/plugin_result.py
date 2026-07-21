from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from models.search_result import SearchResult

if TYPE_CHECKING:
    from plugins.plugin import Plugin


@dataclass(slots=True)
class PluginResult:
    plugin: Plugin
    result: SearchResult
