from __future__ import annotations

from typing import Protocol, Any


class Plugin(Protocol):
    """
    Base plugin interface.
    """

    name: str
    version: str

    def initialize(self) -> None:
        ...

    def shutdown(self) -> None:
        ...


class SearchPlugin(Plugin, Protocol):
    """
    Search strategy plugin.
    """

    def search(self, query: str) -> list[Any]:
        ...


class ScorePlugin(Plugin, Protocol):
    """
    Ranking/scoring plugin.
    """

    def score(self, query: str, document: Any) -> float:
        ...


class FilterPlugin(Plugin, Protocol):
    """
    Search result filter plugin.
    """

    def filter(self, results: list[Any]) -> list[Any]:
        ...


class DownloadPlugin(Plugin, Protocol):
    """
    Downloader abstraction.
    """

    def download(self, url: str) -> bytes:
        ...