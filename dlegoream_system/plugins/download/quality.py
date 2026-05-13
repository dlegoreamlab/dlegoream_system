class BestQuality(QualityPlugin):

    def build_format(self, job: dict) -> str:
        return "bestvideo+bestaudio/best"

class P1080(QualityPlugin):

    def build_format(self, job: dict) -> str:
        return "bestvideo[height<=1080]+bestaudio"

class P720(QualityPlugin):

    def build_format(self, job: dict) -> str:
        return "bestvideo[height<=720]+bestaudio"

class AudioOnly(QualityPlugin):

    def build_format(self, job: dict) -> str:
        return "bestaudio"