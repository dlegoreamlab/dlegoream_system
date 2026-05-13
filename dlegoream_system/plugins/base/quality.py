from dlegoream_system.base.base import Plugin
from dlegoream_system.core.model import FileRecord
from abc import ABC, abstractmethod
from typing import List, Any, Dict

# -------------------------
# 🔹 Quality Plugin
# -------------------------
class QualityPlugin(Plugin):
    """
    출력 포맷 / 품질 구성
    """

    @abstractmethod
    def build_format(self, job: Dict) -> str:
        pass