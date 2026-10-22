# Tests for shared DECK_NAMES and multi-deck note collection. Scope: DeckConfigTests.

import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from anki_utils import get_notes_from_decks
from config import DECK_NAMES
from main import print_progress


class DeckConfigTests(unittest.TestCase):
    # Check DECK_NAMES is a non-empty list of deck names.
    def test_deck_names_is_nonempty_list(self):
        self.assertIsInstance(DECK_NAMES, list)
        self.assertTrue(DECK_NAMES)
        self.assertTrue(all(isinstance(name, str) and name for name in DECK_NAMES))

    # Check notes from multiple decks are de-duplicated.
    def test_notes_from_decks_dedupes(self):
        with mock.patch("anki_utils.get_notes", side_effect=[[1, 2], [2, 3]]):
            self.assertEqual(get_notes_from_decks(["a", "b"]), [1, 2, 3])

    # Check progress shows percent and counts.
    def test_print_progress(self):
        with mock.patch("builtins.print") as mocked_print:
            print_progress(25, 100)
        mocked_print.assert_called_once()
        message = mocked_print.call_args[0][0]
        self.assertIn("25%", message)
        self.assertIn("(25/100)", message)


if __name__ == "__main__":
    unittest.main()
