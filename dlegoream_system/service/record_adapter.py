from dlegoream_system.core.model import FileRecord


class RecordAdapter:
    """
    Simple adapter layer around storage backend.
    """

    def __init__(self, storage):
        self.storage = storage

    def save(self, record: FileRecord):
        self.storage.save(record)
