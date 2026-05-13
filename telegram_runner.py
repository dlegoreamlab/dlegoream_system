import tempfile
import shutil

import asyncio

from dlegoream_system.sources.telegram_source import TelegramPDFSource


API_ID = 12345678
API_HASH = "YOUR_API_HASH"
PHONE = "+8210xxxxxxxx"


async def main():

    source = TelegramPDFSource(
        api_id=API_ID,
        api_hash=API_HASH,
        phone=PHONE
    )

    await source.run()


if __name__ == "__main__":

    asyncio.run(main())
