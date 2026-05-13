from dlegoream_system.base.base import Plugin
from dlegoream_system.core.model import FileRecord
from abc import ABC, abstractmethod

# -------------------------
# 🔹 Filter Plugin
# -------------------------
class FilterPlugin(Plugin):
    """
    필터링 (true/false)
    """

    @abstractmethod
    def match(self, query: str, record: FileRecord) -> bool:
        pass

