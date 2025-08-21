ANKI_CONNECT_URL = "http://127.0.0.1:8765"
DECK_NAME = "testsss"  # Replace with the name of your Anki deck
SOURCE_FIELD = "SentKanji1"  # Field in Anki containing the text to convert to speech
TARGET_FIELD = "Audio"  # Field in Anki where the audio file path will be saved
TTS_SERVICE_URLS = [
    'https://anki.0w0.live/',
    # 'https://ms-ra-forwarder-for-ifreetime-v9q1.vercel.app/'
]  # Replace with the actual TTS service URL
AUDIO_FORMAT = "mp3"  # Desired audio format
BATCH_SIZE = 50  # Number of notes to process in each batch
CACHE_FILE = "audio_cache.json"  # File to store cached audio paths
AUDIO_OUTPUT_DIR = r"C:\\Users\\wwang\\AppData\\Roaming\\Anki2\\User 1\\collection.media"  # Path to save generated audio files

# AUDIO_OUTPUT_DIR = "." 

# TTS parameters for language, voice, and speed
TTS_PARAMS = {
   "voiceName": "ja-JP-KeitaNeural,ja-JP-NanamiNeural",
   "speed": -4,
}

# Add any other necessary configuration settings here