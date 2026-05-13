class TCA_search(SearchPlugin):
    """
    n-gram + 확장 플러그인 기반 검색 엔진
    """

    plugin_name = "tca_search"

    def __init__(self, config=None, extension: SearchExtensionPlugin = None):
        self.config = config or {}
        self.n = self.config.get("n", 2)
        self.depth = self.config.get("depth", 2)

        # 🔥 확장 없으면 기본 확장
        self.extension = extension or NoExtension()

    # -------------------------
    def ngram(self, text: str):
        text = text.replace(" ", "")

        if self.n <= 0 or self.n > len(text):
            return []

        return [text[i:i+self.n] for i in range(len(text) - self.n + 1)]

    # -------------------------
    def preprocess_query(self, query: str):
        return query.strip().lower()

    # -------------------------
    def search(self, query, items, index):

        query = self.preprocess_query(query)

        # 1️⃣ 초기 토큰
        tokens = self.ngram(query)

        # 2️⃣ 초기 후보
        docs = self._collect_docs(tokens, index)

        # 3️⃣ 확장 루프
        for _ in range(self.depth):

            # 🔥 확장 플러그인에 위임
            docs = self.extension.expand(docs, index, tokens)

            if not docs:
                break

            # 🔥 context 재구성
            merged_text = self._merge_docs(docs)

            if not merged_text:
                break

            tokens = self.ngram(merged_text)

            new_docs = self._collect_docs(tokens, index)

            docs.update(new_docs)

        # 4️⃣ scoring (임시)
        return [(doc, 1) for doc in docs]

    # -------------------------
    def _collect_docs(self, tokens, index):
        docs = set()

        for t in tokens:
            if t in index:
                docs.update(index[t])

        return docs

    # -------------------------
    def _merge_docs(self, docs):
        return "".join(sorted(map(str, docs))) if docs else ""