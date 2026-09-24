import tempfile
import unittest
from pathlib import Path

from av_validator.integrity import InputIntegrityError, read_scene_file


class IntegrityTests(unittest.TestCase):
    def test_reader_returns_size_text_and_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.scn"
            path.write_text("/route/main ON\n", encoding="utf-8")
            artifact = read_scene_file(path)
            self.assertEqual(artifact.text, "/route/main ON\n")
            self.assertEqual(artifact.size_bytes, 15)
            self.assertEqual(len(artifact.sha256), 64)

    def test_reader_rejects_non_scene_extension(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_text("/route/main ON\n", encoding="utf-8")
            with self.assertRaisesRegex(InputIntegrityError, ".scn extension"):
                read_scene_file(path)


if __name__ == "__main__":
    unittest.main()
