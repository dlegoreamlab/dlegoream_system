from dlegoream_system.plugins.base import FilterPlugin


class TextFilterPlugin(FilterPlugin):

    def match(self, query, record):
        if not query.text:
            return True
        return query.text.lower() in record.path.lower()