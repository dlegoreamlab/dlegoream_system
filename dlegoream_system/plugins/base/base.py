from abc import ABC, abstractmethod
from typing import List, Any, Dict
from dlegoream_system.core.model import FileRecord


# -------------------------
# 🔹 모든 플러그인 공통 베이스
# -------------------------

class Plugin(ABC):
    """
    모든 플러그인의 최상위 베이스
    """
    plugin_name: str = "base_plugin"