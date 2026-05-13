from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class FileRecord:
    id: str
    path: str
    created_at: float
    updated_at: float
    last_seen: float
    type: str

    # JSON TEXT ↔ dict
    meta: Dict[str, Any] = field(default_factory=dict)