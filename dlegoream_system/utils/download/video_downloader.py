class VideoDownloader:

    def __init__(self, quality_manager, save_path="downloads"):
        self.save_path = save_path
        self.quality_manager = quality_manager
        os.makedirs(self.save_path, exist_ok=True)

    def build_options(self, job):
        fmt = self.quality_manager.get_format(job)

        return {
            "format": fmt,
            "outtmpl": os.path.join(self.save_path, "%(title)s.%(ext)s"),
            "merge_output_format": "mp4",
            "writesubtitles": job.get("subtitle", "n") == "y",
            "writethumbnail": job.get("thumbnail", "n") == "y",
            "noplaylist": job.get("playlist", "n") != "y"
        }

    def download(self, job):
        url = job["url"]

        try:
            with yt_dlp.YoutubeDL(self.build_options(job)) as ydl:
                print(f"다운로드 시작: {url}")
                ydl.download([url])
                print("다운로드 완료")

        except Exception as e:
            print("오류:", e)

    def download_jobs(self, jobs: list):
        for job in jobs:
            self.download(job)