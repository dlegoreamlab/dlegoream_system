from abc import ABC, abstractmethod
from dlegoream_system.base.base import Plugin
from dlegoream_system.core.model import FileRecord


class SearchExtensionPlugin(Plugin):
    plugin_name = "base_extension"

    @abstractmethod
    def expand(self, docs, index, context_tokens):
        pass