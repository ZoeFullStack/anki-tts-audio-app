ANKI_CONNECT_URL = "http://127.0.0.1:8765"
DECK_NAME = "testsss"  # Replace with the name of your Anki deck
SOURCE_FIELD = "SentKanji1"  # Field in Anki containing the text to convert to speech
TARGET_FIELD = "Audio"  # Field in Anki where the audio file path will be saved
TTS_SERVICE_URLS = [
    'https://anki.0w0.live/',
    'https://ms-ra-forwarder-for-ifreetime-v9q1.vercel.app/'
]  # Replace with the actual TTS service URL
AUDIO_FORMAT = "mp3"  # Desired audio format
BATCH_SIZE = 50  # Number of notes to process in each batch
CACHE_FILE = "audio_cache.json"  # File to store cached audio paths
AUDIO_OUTPUT_DIR = r"C:\\Users\\wwang\\AppData\\Roaming\\Anki2\\User 1\\collection.media"  # Path to save generated audio files
# AUDIO_OUTPUT_DIR = "." 


# TTS Configuration
# TTS engine options: 'gtts' (Google TTS, free), 'edge' (Edge TTS, free)
TTS_ENGINE = "gtts"  # Default to using Google TTS

# Google TTS Configuration (used only when TTS_ENGINE = 'gtts')
GTTS_LANGUAGE = "ja"  # Language code: 'ja' for Japanese, 'en' for English, 'zh-CN' for Chinese, etc.
GTTS_TLD = "co.jp"  # Top-level domain for the Google TTS service: 'com', 'co.jp', 'co.uk', etc.

# Edge TTS Configuration (used only when TTS_ENGINE = 'edge')
EDGE_TTS_VOICE = "ja-JP-N anamiNeural"  # Japanese female voice. Other options: ja-JP-KeitaNeural(male), ja-JP-DaichiNeural(male)

# OpenAI TTS Configuration (requires API key - uncomment and modify TTS_ENGINE manually if you want to use this)
# OPENAI_API_KEY = ""  # Your OpenAI API key, can also be set through OPENAI_API_KEY environment variable
# OPENAI_TTS_VOICE = "alloy"  # Options: 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'
# OPENAI_TTS_MODEL = "tts-1"  # Options: 'tts-1', 'tts-1-hd'

# Add any other necessary configuration settings here