from __future__ import annotations

from typing import Protocol, List
from dlegoream_system.core.model import FileRecord


class FileStorage(Protocol):
    """
    Storage interface for file metadata backends.
    """

    def list_files(self, path: str) -> List[str]:
        ...

    def get_records(self, paths: List[str]) -> List[FileRecord]:
        ...

    def save(self, record: FileRecord):
        ...
