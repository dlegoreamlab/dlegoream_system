from dlegoream_system.plugins import SearchPlugin

class TCA_search(SearchPlugin):
    """
    모든 검색 알고리즘의 베이스 클래스
    역할: query 기반 후보군 생성
    """

    plugin_name = "base_search"

    def __init__(self, config=None):
        self.config = config or {}

    @staticmethod
    def ngram(text: str, n: int):
        text = text.replace(" ", "")

        if n <= 0:
            return []
        if n > len(text):
            return []

        return [text[i:i+n] for i in range(len(text) - n + 1)]

    def preprocess_query(self, query: str) -> str:
        return query.strip().lower()

    def search(self, query, items, index):
        """
        후보군 생성 + scoring
        """

        query = self.preprocess_query(query)
        tokens = self.ngram(query, 2)

        score_map = {}

        for token in tokens:
            if token in index:
                for doc_id in index[token]:

                    if doc_id not in score_map:
                        score_map[doc_id] = 0

                    score_map[doc_id] += 1

        # 점수 기준 정렬
        result = sorted(score_map.items(), key=lambda x: x[1], reverse=True)

        # (doc_id, score) 형태 반환
        return result

    def validate_items(self, items):
        if items is None:
            return []

        if not isinstance(items, list):
            raise TypeError("items must be list")

        return items