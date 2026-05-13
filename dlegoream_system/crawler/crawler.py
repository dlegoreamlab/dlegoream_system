class SimpleCrawler:

    def __init__(self, adapter):
        self.adapter = adapter

    def crawl(self, url):
        html = self.fetch(url)
        record = self.to_record(url, html)

        # ✔ 여기서 끝
        self.adapter.save(record)