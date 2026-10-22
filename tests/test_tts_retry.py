# Tests for gTTS retry and per-note skip-on-failure. Scope: TtsRetryTests.

import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import process_field_pair
from tts_utils import save_gtts_with_retry


class TtsRetryTests(unittest.TestCase):
    # Retry gTTS and succeed on the last attempt.
    def test_gtts_retries_then_succeeds(self):
        tts = mock.Mock()
        tts.save.side_effect = [Exception("empty 200"), None]
        with mock.patch("tts_utils.gTTS", return_value=tts), mock.patch("tts_utils.time.sleep"):
            save_gtts_with_retry("hello", "/tmp/a.mp3", "en", "com")
        self.assertEqual(tts.save.call_count, 2)

    # Skip one failed field instead of crashing the batch.
    def test_process_field_pair_skips_failure(self):
        fields = {
            "frontSentence": {"value": "hello"},
            "frontAudio": {"value": ""},
        }
        with mock.patch("main.generate_and_store_audio", side_effect=Exception("gTTS down")):
            self.assertFalse(process_field_pair(1, fields, "frontSentence", "frontAudio"))


if __name__ == "__main__":
    unittest.main()
