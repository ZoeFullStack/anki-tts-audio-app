ANKI_CONNECT_URL = "http://127.0.0.1:8765"
DECK_NAME = "speak"

TTS_SERVICE_URLS = [
    "https://anki.0w0.live/",
    "https://ms-ra-forwarder-for-ifreetime-v9q1.vercel.app/",
]
AUDIO_FORMAT = "mp3"
BATCH_SIZE = 50
CACHE_FILE = "audio_cache.json"
# 音频通过 AnkiConnect 存入当前用户的媒体目录，无需配置本机路径。

# TTS engine options: 'gtts' (Google TTS, free), 'edge' (Edge TTS, free)
TTS_ENGINE = "gtts"
# True：已有音频的字段跳过。手机播不了时改 False 再跑一遍以重新生成。
SKIP_EXISTING_AUDIO = True

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
