import asyncio

from dlegoream_system.plugins.quality import (
    BestQuality,
    P1080,
    P720,
    AudioOnly
)

from dlegoream_system.plugins.base import ScoringPlugin

from managers import QualityManager, ScoreManager

# 너가 이미 만든 것들
from crawler.simple_crawler import SimpleCrawler
from downloader.video_downloader import VideoDownloader

from models import SearchQuery


# =========================
# 1. 초기화
# =========================

quality_manager = QualityManager()
score_manager = ScoreManager()

crawler = SimpleCrawler()
downloader = VideoDownloader()


# =========================
# 2. 플러그인 등록
# =========================

# quality
quality_manager.register("best", BestQuality())
quality_manager.register("1080", P1080())
quality_manager.register("720", P720())
quality_manager.register("audio", AudioOnly())


# score (너 SimpleScorePlugin 그대로 사용)
from your_score_file import SimpleScorePlugin

score_manager.register(SimpleScorePlugin())


# =========================
# 3. 엔진 파이프라인
# =========================

async def run_pipeline(query_text: str):

    query = SearchQuery(text=query_text)

    print("🔎 crawling 시작...")

    # 1) 크롤링 or source 실행
    records = crawler.explore(query.text)

    print(f"📦 {len(records)}개 수집됨")

    results = []

    # 2) score filtering
    for record in records:

        score = score_manager.calculate(
            query.text,
            record
        )

        record.score = score

        if score < 0.3:
            continue

        results.append(record)

    print(f"⭐ 필터 후: {len(results)}개")

    # 3) download job 생성
    for record in results:

        job = {
            "url": record.path,
            "quality": "1080"
        }

        fmt = quality_manager.get_format(job)
        job["format"] = fmt

        print(f"⬇ download: {record.path} | score={record.score}")

        downloader.download(job)

    print("✅ 완료")


# =========================
# 4. 실행
# =========================

if __name__ == "__main__":

    asyncio.run(
        run_pipeline("ai research paper")
    )