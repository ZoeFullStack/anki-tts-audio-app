import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from language_utils import normalize_tts_text, strip_html


class NormalizeTtsTextTests(unittest.TestCase):
    def test_contraction_apostrophes(self):
        expected = "How come you haven't gone home yet?"
        for apostrophe in ["'", "’", "‘", "ʼ", "＇", "`", "´"]:
            with self.subTest(apostrophe=apostrophe):
                self.assertEqual(
                    normalize_tts_text(expected.replace("'", apostrophe)), expected
                )

    def test_html_encoded_apostrophes(self):
        for entity in ["&#39;", "&#x27;", "&apos;", "&rsquo;", "&#8217;", "&amp;#39;", "&amp;rsquo;"]:
            with self.subTest(entity=entity):
                self.assertEqual(normalize_tts_text(f"haven{entity}t"), "haven't")

    def test_anki_html(self):
        self.assertEqual(
            normalize_tts_text(strip_html("<div>How come you haven&rsquo;t gone home yet?</div>")),
            "How come you haven't gone home yet?",
        )

    def test_preserves_other_text(self):
        for text in ["I'm sure it's John's.", "彼は「まだ？」と言った。", "‘Hello’", "Price: ¥100", "3′ 5″"]:
            with self.subTest(text=text):
                self.assertEqual(normalize_tts_text(text), text)


if __name__ == "__main__":
    unittest.main()
