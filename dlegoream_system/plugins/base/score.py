from dlegoream_system.base.base import Plugin
from dlegoream_system.core.model import FileRecord
from abc import ABC, abstractmethod

# -------------------------
# 🔹 Scoring Plugin
# -------------------------
class ScoringPlugin(Plugin):
    """
    후보 정렬용 점수 계산
    """

    @abstractmethod
    def score(self, query: str, record: FileRecord) -> float:
        pass
