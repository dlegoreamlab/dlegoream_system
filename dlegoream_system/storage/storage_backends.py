import sqlite3
import json
from typing import List, Optional

from dlegoream_system.core.model import FileRecord
from dlegoream_system.core.storage import FileStorage


class SQLiteStorage(FileStorage):

    def __init__(self, db_path="metadata.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_table()

    def _init_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id TEXT PRIMARY KEY,
            path TEXT,
            created_at REAL,
            updated_at REAL,
            last_seen REAL,
            type TEXT,
            meta TEXT
        )
        """)

        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_path ON files(path)")
        self.conn.commit()

    # ✔ 단순 조회
    def list_files(self, path: str) -> List[str]:
        self.cursor.execute(
            "SELECT path FROM files WHERE path LIKE ?",
            (f"{path}%",)
        )
        return [r[0] for r in self.cursor.fetchall()]

    # ✔ batch fetch
    def get_records(self, paths: List[str]) -> List[FileRecord]:
        if not paths:
            return []

        q = f"""
        SELECT id, path, created_at, updated_at,
               last_seen, type, meta
        FROM files
        WHERE path IN ({",".join(["?"] * len(paths))})
        """

        self.cursor.execute(q, paths)
        rows = self.cursor.fetchall()

        return [
            FileRecord(
                id=r[0],
                path=r[1],
                created_at=r[2],
                updated_at=r[3],
                last_seen=r[4],
                type=r[5],
                meta=json.loads(r[6]) if r[6] else {},
            )
            for r in rows
        ]

    # ✔ 안전한 fetch
    def fetch_one(self, column: str, value):

        allowed = {"id", "path", "type", "created_at"}

        if column not in allowed:
            raise ValueError("Invalid column")

        self.cursor.execute(
            f"SELECT * FROM files WHERE {column}=?",
            (value,)
        )

        return self.cursor.fetchone()

    # ✔ 핵심: storage는 "파일 시스템 체크 안함"
    def save(self, record: FileRecord):

        row = self.fetch_one("path", record.path)

        if row is None:
            self.cursor.execute("""
            INSERT INTO files (
                id, path, created_at, updated_at, last_seen, type, meta
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                record.id,
                record.path,
                record.created_at,
                record.updated_at,
                record.last_seen,
                record.type,
                json.dumps(record.meta)
            ))
        else:
            self.cursor.execute("""
            UPDATE files
            SET updated_at=?,
                last_seen=?,
                type=?,
                meta=?
            WHERE path=?
            """, (
                record.updated_at,
                record.last_seen,
                record.type,
                json.dumps(record.meta),
                record.path
            ))

        self.conn.commit()