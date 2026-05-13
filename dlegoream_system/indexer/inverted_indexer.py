# indexer.py

import re
import json
from collections import defaultdict
from typing import List, Dict, Any


class InvertedIndexer:
    """
    역색인 생성기
    - doc_id -> text
    - token -> [doc_id, ...]
    """

    def __init__(self, min_ngram: int = 2):
        self.min_ngram = min_ngram
        self.index = defaultdict(set)   # token -> set(doc_id)

    # -------------------------
    # 🔹 토큰화 (아주 단순 버전)
    # -------------------------
    def tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r"[^a-z0-9가-힣 ]", " ", text)
        tokens = text.split()
        return tokens

    # -------------------------
    # 🔹 ngram (옵션)
    # -------------------------
    def ngrams(self, token: str) -> List[str]:
        if len(token) < self.min_ngram:
            return [token]

        return [
            token[i:i + self.min_ngram]
            for i in range(len(token) - self.min_ngram + 1)
        ]

    # -------------------------
    # 🔹 문서 추가
    # -------------------------
    def add_document(self, doc_id: int, text: str):
        tokens = self.tokenize(text)

        for token in tokens:
            # 기본 토큰
            self.index[token].add(doc_id)

            # ngram 확장 (옵션)
            for ng in self.ngrams(token):
                self.index[ng].add(doc_id)

    # -------------------------
    # 🔹 bulk indexing
    # -------------------------
    def build(self, documents: Dict[int, str]):
        for doc_id, text in documents.items():
            self.add_document(doc_id, text)

    # -------------------------
    # 🔹 저장 (JSON)
    # -------------------------
    def save(self, path: str):
        serializable = {
            token: list(doc_ids)
            for token, doc_ids in self.index.items()
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, ensure_ascii=False, indent=2)

    # -------------------------
    # 🔹 로드
    # -------------------------
    def load(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.index = {
            token: set(doc_ids)
            for token, doc_ids in data.items()
        }

    # -------------------------
    # 🔹 검색 (테스트용)
    # -------------------------
    def search(self, query: str) -> List[int]:
        tokens = self.tokenize(query)

        result_sets = []

        for token in tokens:
            if token in self.index:
                result_sets.append(self.index[token])

        if not result_sets:
            return []

        # AND 검색
        result = set.intersection(*result_sets)
        return list(result)