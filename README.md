
# dlegoream

Telegram PDF crawler + metadata indexing + search engine.

---

# Features

- Telegram multi-channel PDF crawler
- Automatic resume support
- SQLite metadata storage
- Search engine architecture
- Plugin scoring/filter system
- File indexing
- Persistent progress tracking
- Searchable PDF archive foundation

---

# Architecture

```text
Telegram
↓
TelegramPDFSource
↓
PDF Download
↓
FileRecord
↓
SQLiteStorage
↓
SearchEngine
↓
Search Results
```

---

# Project Structure

```text
dlegoream/
├── main.py
├── telegram_runner.py
├── README.md
│
├── dlegoream_system/
│   ├── core/
│   │   ├── engine.py
│   │   ├── indexer.py
│   │   ├── model.py
│   │   └── storage.py
│   │
│   ├── storage/
│   │   └── storage_backends.py
│   │
│   ├── plugins/
│   │   └── manager.py
│   │
│   ├── service/
│   │   └── record_adapter.py
│   │
│   ├── sources/
│   │   └── telegram_source.py
│   │
│   └── config/
```

---

# Installation

## Python

Recommended:

- Python 3.10+
- SQLite

---

# Install Dependencies

```bash
pip install telethon
pip install sqlalchemy
pip install pymupdf
```

Optional:

```bash
pip install pdfplumber
```

---

# Telegram Setup

Go to:

https://my.telegram.org

Create:

- api_id
- api_hash

---

# Configure Telegram

Edit:

```python
telegram_runner.py
```

Set:

```python
API_ID = 12345678
API_HASH = "YOUR_API_HASH"
PHONE = "+8210xxxxxxxx"
```

---

# channels.json

Create:

```json
{
    "channels": [
        {
            "name": "papers",
            "link": "https://t.me/example"
        }
    ]
}
```

---

# Run Telegram Crawler

```bash
python3 telegram_runner.py
```

---

# Download Flow

```text
Telegram Channel
→ PDF Detection
→ Download
→ Metadata Extraction
→ SQLite Save
→ Searchable Archive
```

---

# FileRecord Structure

```python
FileRecord(
    id="tg-channel-messageid",
    path="/pdfs/file.pdf",
    created_at=timestamp,
    updated_at=timestamp,
    last_seen=timestamp,
    type="telegram_pdf",
    meta={
        "source": "telegram",
        "channel": "papers",
        "telegram_message_id": 12345,
        "mime": "application/pdf",
        "size": 123456,
        "file_name": "paper.pdf"
    }
)
```

---

# Search Example

```python
from dlegoream_system.core.engine import SearchEngine
from dlegoream_system.plugins.manager import PluginManager
from dlegoream_system.storage.storage_backends import SQLiteStorage
from dlegoream_system.core.model import SearchQuery

storage = SQLiteStorage()

engine = SearchEngine(
    storage,
    PluginManager()
)

results = engine.search(
    query=SearchQuery(text="algebra"),
    path="private_pdfs"
)

for r in results:
    print(r.record.path)
```

---

# Directory Indexing

```python
from dlegoream_system.core.indexer import index_directory

index_directory(
    storage,
    "/documents"
)
```

---

# Plugin System

## Scorer Example

```python
class SimpleScorer:

    def score(self, query, record):

        content = record.meta.get("content", "")

        if query.text in content:
            return 10.0

        return 0.0
```

Register:

```python
pm.register_scorer(
    SimpleScorer()
)
```

---

# Filter Example

```python
class PDFFilter:

    def filter(self, query, record):

        return record.path.endswith(".pdf")
```

Register:

```python
pm.register_filter(
    PDFFilter()
)
```

---

# Current Capabilities

Working:

- Telegram crawling
- PDF downloading
- SQLite metadata storage
- Resume support
- Search architecture
- Plugin architecture
- File indexing

Not yet implemented:

- BM25 ranking
- Full text indexing
- Vector embeddings
- OCR
- Semantic search
- Async queue workers
- Real relevance scoring
- Automatic plugin loading

---

# Recommended Next Steps

## 1. PDF Text Extraction

Recommended:

```bash
pip install pymupdf
```

Example:

```python
import fitz

doc = fitz.open(pdf_path)

text = ""

for page in doc:
    text += page.get_text()
```

Store:

```python
meta["content"] = text
```

---

# Result

Then:

```python
SearchQuery(text="machine learning")
```

Can search inside PDF contents.

---

# Recommended Future Architecture

```text
Telegram
+
Discord
+
Google Drive
+
Local Files
+
Web Crawlers

↓ unified ↓

dlegoream Search Engine
```

---

# Android / Termux

Install:

```bash
pkg install python
pip install telethon sqlalchemy pymupdf
```

Run:

```bash
python3 telegram_runner.py
```

---

# Notes

- Progress saved in:
  - progress.json

- PDFs stored in:
  - private_pdfs/

- Session stored in:
  - session_multi.session

- SQLite backend used for metadata persistence.

---

# License

Personal / experimental project.
