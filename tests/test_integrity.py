import tempfile
import unittest
from pathlib import Path

from av_validator.integrity import InputIntegrityError, read_scene_file


class IntegrityTests(unittest.TestCase):
    def test_reader_returns_size_text_and_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.scn"
            path.write_bytes(b"/route/main ON\n")
            artifact = read_scene_file(path)
            self.assertEqual(artifact.text, "/route/main ON\n")
            self.assertEqual(artifact.size_bytes, 15)
            self.assertEqual(len(artifact.sha256), 64)

    def test_reader_rejects_non_scene_extension(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_bytes(b"/route/main ON\n")
            with self.assertRaisesRegex(InputIntegrityError, ".scn extension"):
                read_scene_file(path)

    def test_reader_rejects_oversized_scene(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "large.scn"
            path.write_bytes(b"12345")
            with self.assertRaisesRegex(InputIntegrityError, "size limit"):
                read_scene_file(path, max_bytes=4)

    def test_reader_rejects_invalid_utf8(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.scn"
            path.write_bytes(b"\xff\xfe")
            with self.assertRaisesRegex(InputIntegrityError, "valid UTF-8"):
                read_scene_file(path)

    def test_reader_rejects_missing_scene(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing.scn"
            with self.assertRaisesRegex(InputIntegrityError, "does not exist"):
                read_scene_file(path)


if __name__ == "__main__":
    unittest.main()
