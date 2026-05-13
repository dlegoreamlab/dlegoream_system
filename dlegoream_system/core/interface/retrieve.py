from __future__ import annotations

from typing import Protocol, Any


class Retriever(Protocol):
    """
    Generic retrieval interface.
    """

    def retrieve(self, query: str, limit: int = 10) -> list[Any]:
        ...


class SemanticRetriever(Retriever, Protocol):
    """
    Embedding/vector retrieval.
    """

    def embed(self, text: str) -> list[float]:
        ...


class HybridRetriever(Retriever, Protocol):
    """
    BM25 + semantic retrieval.
    """

    def lexical_search(self, query: str) -> list[Any]:
        ...

    def semantic_search(self, query: str) -> list[Any]:
        ...