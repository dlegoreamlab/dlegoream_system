from dataclasses import dataclass, field
from typing import Dict, Optional, Any


@dataclass
class SearchQuery:
    text: Optional[str] = None


@dataclass
class FileRecord:
    id: str
    path: str
    created_at: float
    updated_at: float
    last_seen: float
    type: str
    meta: Dict[str, Any] = field(default_factory=dict)
    score: float = 0.0


@dataclass
class SearchResult:
    record: FileRecord
    score: float = 0.0
    last_seen: float = 0.0