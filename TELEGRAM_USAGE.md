
# Telegram PDF Integration

## Install

pip install telethon

## Configure

Edit:

telegram_runner.py

Set:

- API_ID
- API_HASH
- PHONE

## channels.json example

{
    "channels": [
        {
            "name": "papers",
            "link": "https://t.me/example"
        }
    ]
}

## Run

python3 telegram_runner.py

## Result

Downloaded PDFs are:

private_pdfs/

Metadata stored in SQLite via:

SQLiteStorage()

Searchable through:

SearchEngine()
