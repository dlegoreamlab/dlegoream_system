import tempfile
import shutil

import os
import json
import asyncio
import random
from datetime import datetime

from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeFilename
from telethon.errors import FloodWaitError

from dlegoream_system.core.model import FileRecord
from dlegoream_system.storage.storage_backends import SQLiteStorage


class TelegramPDFSource:

    def __init__(
        self,
        api_id,
        api_hash,
        phone,
        download_folder="private_pdfs",
        channels_json="channels.json",
        progress_file="progress.json"
    ):

        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone

        self.download_folder = download_folder
        self.channels_json = channels_json
        self.progress_file = progress_file

        os.makedirs(download_folder, exist_ok=True)

        self.client = TelegramClient(
            "session_multi",
            api_id,
            api_hash
        )

        self.storage = SQLiteStorage()

        self.downloaded = set()

        self.download_count = 0
        self.hourly_count = 0
        self.last_hour_reset = asyncio.get_event_loop().time()

        self.MAX_DOWNLOADS_PER_HOUR = 65
        self.DELAY_BETWEEN_FILES = (3.5, 8.0)

    def load_channels(self):

        with open(self.channels_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data.get("channels", [])

    def load_progress(self):

        if not os.path.exists(self.progress_file):
            return {}

        with open(self.progress_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_progress(self, progress):

        temp_fd, temp_path = tempfile.mkstemp(
            prefix="progress_",
            suffix=".tmp"
        )

        try:

            with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
                json.dump(
                    progress,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

                f.flush()
                os.fsync(f.fileno())

            shutil.move(temp_path, self.progress_file)

        finally:

            if os.path.exists(temp_path):
                os.remove(temp_path)

def safe_download(self, message, channel_name, channel_link):

        if not message.document:
            return False

        doc = message.document

        is_pdf = doc.mime_type == "application/pdf"

        if not is_pdf:

            for attr in doc.attributes:

                if isinstance(attr, DocumentAttributeFilename):

                    if (
                        attr.file_name and
                        attr.file_name.lower().endswith(".pdf")
                    ):

                        is_pdf = True
                        break

        if not is_pdf:
            return False

        file_name = None

        for attr in doc.attributes:

            if isinstance(attr, DocumentAttributeFilename):
                file_name = attr.file_name
                break

        if not file_name:
            file_name = f"pdf_{message.id}.pdf"

        safe_name = f"[{channel_name}]_{file_name}"

        file_path = os.path.join(
            self.download_folder,
            safe_name
        )

        if (
            os.path.exists(file_path) or
            safe_name in self.downloaded
        ):
            return False

        print(f"↓ [{channel_name}] {file_name}")

        try:

            await message.download_media(file=file_path)

            self.downloaded.add(safe_name)

            self.download_count += 1
            self.hourly_count += 1

            record = FileRecord(
                id=f"tg-{channel_name}-{message.id}",
                path=file_path,
                created_at=datetime.now().timestamp(),
                updated_at=datetime.now().timestamp(),
                last_seen=datetime.now().timestamp(),
                type="telegram_pdf",
                meta={
                    "source": "telegram",
                    "channel": channel_name,
                    "channel_link": channel_link,
                    "telegram_message_id": message.id,
                    "mime": doc.mime_type,
                    "size": doc.size,
                    "file_name": file_name
                }
            )

            self.storage.save(record)

            print(f"✅ 저장 완료: {file_name}")

            return True

        except FloodWaitError as e:

            print(f"FloodWait: {e.seconds}초")
            await asyncio.sleep(e.seconds + 5)

        except Exception as e:

            print(f"다운로드 실패: {e}")

        return False

    async def crawl_channel(self, channel_info, progress):

        channel_name = channel_info["name"]
        channel_link = channel_info["link"]

        last_id = progress.get(
            channel_link,
            {}
        ).get(
            "last_message_id",
            0
        )

        print(f"▶ {channel_name} 시작")

        entity = await self.client.get_entity(channel_link)

        async for message in self.client.iter_messages(
            entity,
            limit=None,
            reverse=False,
            min_id=last_id
        ):

            success = await self.safe_download(
                message,
                channel_name,
                channel_link
            )

            if success:

                await asyncio.sleep(
                    random.uniform(
                        self.DELAY_BETWEEN_FILES[0],
                        self.DELAY_BETWEEN_FILES[1]
                    )
                )

            if message.id > last_id:

                last_id = message.id

                progress[channel_link] = {
                    "channel_name": channel_name,
                    "last_message_id": last_id,
                    "last_updated": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                }

                if self.download_count % 10 == 0:
                    self.save_progress(progress)

        self.save_progress(progress)

    async def run(self):

        await self.client.start(phone=self.phone)

        channels = self.load_channels()

        progress = self.load_progress()

        tasks = [
            self.crawl_channel(ch, progress)
            for ch in channels
        ]

        await asyncio.gather(*tasks)

        print(f"총 다운로드: {self.download_count}")


# Stability patch helper
def cleanup_partial_file(file_path):
    part = file_path + ".part"
    if os.path.exists(part):
        os.remove(part)
