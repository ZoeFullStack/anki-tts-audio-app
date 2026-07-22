ANKI_CONNECT_URL = "http://127.0.0.1:8765"
DECK_NAME = "pte"

TTS_SERVICE_URLS = [
    "https://anki.0w0.live/",
    "https://ms-ra-forwarder-for-ifreetime-v9q1.vercel.app/",
]
AUDIO_FORMAT = "mp3"
BATCH_SIZE = 50
CACHE_FILE = "audio_cache.json"
AUDIO_OUTPUT_DIR = r"C:\Users\Developer\AppData\Roaming\Anki2\User 1\collection.media"

# TTS engine options: 'gtts' (Google TTS, free), 'edge' (Edge TTS, free)
TTS_ENGINE = "gtts"

# 多组字段映射：从 source 读取文字，生成语音写入 target
FIELD_MAPPINGS = [
    {"source": "frontSentence", "target": "frontAudio"},
    {"source": "backMeaning", "target": "backAudio"},
]

# 按检测到的语言选择 TTS 参数
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
