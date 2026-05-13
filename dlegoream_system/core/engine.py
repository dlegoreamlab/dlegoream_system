import time
from typing import List

from dlegoream_system.core.model import SearchQuery, SearchResult
from dlegoream_system.config.meta_schema import META_SCHEMA
from dlegoream_system.core.storage import FileStorage
from dlegoream_system.plugins.manager import PluginManager


class SearchEngine:

    def __init__(self, storage: FileStorage, plugin_manager: PluginManager):
        self.storage = storage
        self.pm = plugin_manager

    def _score(self, query, record):
        """
        1. plugin scoring
        2. schema scoring fields 반영
        """

        base_score = self.pm.apply_scorers(query, record)

        schema = META_SCHEMA.get(record.type, {})

        # ✔ schema scoring 반영
        for field in schema.get("scoring", []):
            value = record.meta.get(field)

            if isinstance(value, (int, float)):
                base_score += value * 0.1

        return base_score

    def _recommend(self, record):
        """
        video 같은 경우 추천 필드 처리
        """
        schema = META_SCHEMA.get(record.type, {})

        return record.meta.get(
            schema.get("recommend", [None])[0]
            if schema.get("recommend") else None
        )

    def search(self, query: SearchQuery, path: str):

        paths = self.storage.list_files(path)
        records = self.storage.get_records(paths)

        results = []
        now = time.time()

        for r in records:

            # ✔ filter 단계
            if not self.pm.apply_filters(query, r):
                continue

            # ✔ score 단계
            score = self._score(query, r)

            # ✔ 추천 데이터 (video만 의미 있음)
            recommend = self._recommend(r)

            # score 반영
            r.score = score

            # 결과 생성
            results.append(SearchResult(
                record=r,
                score=score,
                last_seen=r.last_seen
            ))

        return sorted(results, key=lambda x: x.score, reverse=True)