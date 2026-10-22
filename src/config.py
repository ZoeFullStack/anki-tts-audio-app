# Shared Anki/TTS settings used by audio generation and auto-suspend. Scope: constants only.

ANKI_CONNECT_URL = "http://127.0.0.1:8765"
# Shared deck list for TTS generation and auto-suspend; supports multiple decks.
DECK_NAMES = ["speak", "word"]

TTS_SERVICE_URLS = [
    "https://anki.0w0.live/",
    "https://ms-ra-forwarder-for-ifreetime-v9q1.vercel.app/",
]
AUDIO_FORMAT = "mp3"
BATCH_SIZE = 50
CACHE_FILE = "audio_cache.json"
# Audio is stored via AnkiConnect; no local media path is required.

# TTS engine options: 'gtts' (Google TTS, free), 'edge' (Edge TTS, free)
TTS_ENGINE = "gtts"
# Skip fields that already have audio. Set False to regenerate for mobile playback.
SKIP_EXISTING_AUDIO = True
# gTTS rate-limit handling for large decks.
TTS_RETRY = 3
TTS_RETRY_SLEEP = 2
TTS_REQUEST_SLEEP = 1

# Map source text fields to target audio fields.
FIELD_MAPPINGS = [
    {"source": "frontSentence", "target": "frontAudio"},
    {"source": "backMeaning", "target": "backAudio"},
]

# TTS params selected by detected language.
TTS_LANGUAGE_CONFIG = {
    "ja": {
        "gtts_lang": "ja",
        "gtts_tld": "co.jp",
        "edge_voice": "ja-JP-NanamiNeural",
    },
    "en": {
        "gtts_lang": "en",
        "gtts_tld": "com",
        "edge_voice": "en-US-GuyNeural",
    },
}
