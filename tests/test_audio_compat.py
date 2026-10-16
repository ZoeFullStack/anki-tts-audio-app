import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from audio_compat import ensure_mobile_compatible_audio, with_converted_suffix
from tts_utils import text_to_speech


class AudioCompatTests(unittest.TestCase):
    def test_suffix_follows_converted_file(self):
        self.assertEqual(
            with_converted_suffix("hello_en_gtts_1_local.mp3", "/tmp/audio.m4a"),
            "hello_en_gtts_1_local.m4a",
        )

    def test_gtts_converts_to_playable_m4a(self):
        with tempfile.TemporaryDirectory(prefix="anki-tts-test-") as temp_dir:
            mp3_path = str(Path(temp_dir) / "audio.mp3")
            text_to_speech(
                text="Hello, this is a test.",
                audio_file_path=mp3_path,
                lang="en",
                engine="gtts",
                voice="com",
            )
            converted = ensure_mobile_compatible_audio(mp3_path)
            self.assertTrue(converted.endswith(".m4a"))
            self.assertGreater(Path(converted).stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
