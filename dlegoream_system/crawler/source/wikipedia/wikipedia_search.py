import wikipediaapi


class WikipediaSearch:

    def __init__(self, lang="en"):
        self.wiki = wikipediaapi.Wikipedia(
            user_agent="dlegoream/1.0",
            language=lang
        )

    def search(self, title: str):

        page = self.wiki.page(title)

        if not page.exists():
            return None

        sections = []

        for sec in page.sections:

            sections.append({
                "title": sec.title,
                "text": sec.text,
                "links": list(sec.links.keys()) if sec.links else [],
                "images": []
            })

        return {
            "title": page.title,
            "summary": page.summary,
            "sections": sections,
            "images": list(page.images)[:10]
        }