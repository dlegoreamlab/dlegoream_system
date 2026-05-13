import arxiv

from dlegoream_system.core.model import (
    SearchQuery
)


class ArxivSearchPlugin:

    def __init__(
        self,
        max_results=10
    ):

        self.max_results = (
            max_results
        )

    def search(
        self,
        query: SearchQuery
    ) -> list[str]:

        search = arxiv.Search(

            query=query.text,

            max_results=(
                self.max_results
            ),

            sort_by=(
                arxiv
                .SortCriterion
                .Relevance
            )
        )

        pdf_urls = []

        for result in (
            search.results()
        ):

            pdf_urls.append(
                result.pdf_url
            )

        return pdf_urls