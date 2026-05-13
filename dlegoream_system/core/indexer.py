import os
import time
import uuid

from dlegoream_system.core.model import FileRecord
from dlegoream_system.core.storage import FileStorage


def index_directory(storage: FileStorage, base_path: str):
    """
    Scan the filesystem and store metadata records.
    """

    for root, _, files in os.walk(base_path):

        for file_name in files:

            path = os.path.join(root, file_name)

            now = time.time()

            record = FileRecord(
                id=str(uuid.uuid4()),
                path=path,
                created_at=now,
                updated_at=now,
                last_seen=now,
                type=os.path.splitext(file_name)[1].lstrip(".") or "unknown",
                meta={}
            )

            storage.save(record)
