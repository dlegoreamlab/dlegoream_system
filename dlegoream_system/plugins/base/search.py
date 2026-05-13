from abc import ABC, abstractmethod

class SearchPlugin(ABC):
    plugin_name = "base_search"

    @abstractmethod
    def search(self, query, items, index):
        pass