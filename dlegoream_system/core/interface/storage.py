from __future__ import annotations

from typing import Protocol, Iterable, Optional, Any


class StorageBackend(Protocol):
    """
    Generic storage backend interface.
    """

    def save(self, key: str, value: Any) -> None:
        ...

    def load(self, key: str) -> Optional[Any]:
        ...

    def delete(self, key: str) -> None:
        ...

    def exists(self, key: str) -> bool:
        ...

    def keys(self) -> Iterable[str]:
        ...


class IndexStorage(Protocol):
    """
    Inverted index persistence layer.
    """

    def add_term(self, term: str, document_id: str) -> None:
        ...

    def get_postings(self, term: str) -> list[str]:
        ...

    def flush(self) -> None:
        ...