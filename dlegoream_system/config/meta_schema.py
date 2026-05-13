META_SCHEMA = {
    "music": {
        "fields": [
            "play_score",
            "artist",
            "album",
            "genre",
            "duration"
        ]
    },

    "pdf": {
        "fields": [
            "title",
            "source_url",
            "snippet",
            "page_count",
            "language"
        ],
        "scoring": [
            "relevance",
            "freshness"
        ]
    },

    "video": {
        "fields": [
            "title",
            "series",
            "genre",
            "duration",
            "size"
        ],
        "recommend": [
            "next_related"
        ]
    }
}