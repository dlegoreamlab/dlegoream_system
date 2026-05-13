import traceback


class PluginManager:
    """
    Minimal plugin manager implementation.
    """

    def __init__(self):
        self.filters = []
        self.scorers = []

    def register_filter(self, plugin):
        self.filters.append(plugin)

    def register_scorer(self, plugin):
        self.scorers.append(plugin)

    def apply_filters(self, query, record):

        for plugin in self.filters:

            try:

                if not plugin.filter(query, record):
                    return False

            except Exception as e:

                print(
                    f"[FILTER ERROR] {plugin.__class__.__name__}: {e}"
                )

                traceback.print_exc()

                continue

        return True

    def apply_scorers(self, query, record):

        total = 0.0

        for plugin in self.scorers:

            try:

                score = plugin.score(query, record)

                if isinstance(score, (int, float)):
                    total += score

            except Exception as e:

                print(
                    f"[SCORER ERROR] {plugin.__class__.__name__}: {e}"
                )

                traceback.print_exc()

                continue

        return total
