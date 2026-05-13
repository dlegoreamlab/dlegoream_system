from abc import ABC, abstractmethod
from typing import List
from dlegoream_system.core.model import FileRecord


class FileStorage(ABC):

    @abstractmethod
    def list_files(self, path: str) -> List[str]:
        pass

    @abstractmethod
    def get_records(self, paths: List[str]) -> List[FileRecord]:
        pass

    @abstractmethod
    def fetch_one(self, column: str, value):
        pass

    @abstractmethod
    def save(self, record: FileRecord):
        pass