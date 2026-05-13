from __future__ import annotations

from typing import Protocol, Iterable, Any


class CrawlSource(Protocol):
    """
    Single crawl source.
    """

    name: str

    def fetch(self) -> Iterable[Any]:
        ...


class Crawler(Protocol):
    """
    Main crawler interface.
    """

    def register_source(self, source: CrawlSource) -> None:
        ...

    def crawl(self) -> Iterable[Any]:
        ...