from __future__ import annotations

from typing import Protocol, Any


class Scorer(Protocol):
    """
    Ranking abstraction.
    """

    def score(self, query: str, document: Any) -> float:
        ...


class WeightedScorer(Scorer, Protocol):
    """
    Weighted score support.
    """

    weight: float