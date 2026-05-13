import time

from dlegoream_system.storage.storage_backends import SQLiteStorage
from dlegoream_system.service.record_adapter import RecordAdapter
from dlegoream_system.core.engine import SearchEngine
from dlegoream_system.plugins.manager import PluginManager
from dlegoream_system.core.model import FileRecord, SearchQuery


storage = SQLiteStorage()

adapter = RecordAdapter(storage)

pm = PluginManager()

engine = SearchEngine(storage, pm)

record = FileRecord(
    id="test-2",
    path="/storage/emulated/0/project/main.py",
    created_at=time.time(),
    updated_at=time.time(),
    last_seen=time.time(),
    type="local",
    meta={"content": "hello engine"}
)

adapter.save(record)

query = SearchQuery(text="test")

results = engine.search(
    query=query,
    path="/storage/emulated/0/project"
)

print("SEARCH RESULT:")

for r in results:
    print(r.record.path, r.score)
