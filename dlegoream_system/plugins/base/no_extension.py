from dlegoream_system.plugins.base.extension import SearchExtensionPlugin

class NoExtension(SearchExtensionPlugin):
    plugin_name = "no_extension"

    def expand(self, docs, index, context_tokens):
        return docs