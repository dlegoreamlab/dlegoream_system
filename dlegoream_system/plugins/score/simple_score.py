import json
from dlegoream_system.plugins.base import ScoringPlugin


class SimpleScorePlugin(ScoringPlugin):

    def __init__(self, config_path="config.json"):

        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.weights = self.config.get("weights", {})

    def score(self, query, record):

        query = query.lower()
        score = 0.0

        # path score
        path_weight = self.weights.get("path", 0)
        if query in record.path.lower():
            score += path_weight

        # title score
        weight_2 = self.weights.get("title", 0)
        title = record.meta.get("title", "").lower()
        if query in title:
            score += weight_2

        return min(score, 1.0)