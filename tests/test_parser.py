import unittest

from av_validator.parser import SceneParseError, parse_scene_text


class ParserTests(unittest.TestCase):
    def test_parser_preserves_path_and_quoted_value(self):
        parsed = parse_scene_text('/ch/01/config "Pastor Mic" 1 LOCAL\n')
        self.assertEqual(parsed["/ch/01/config"], ("Pastor Mic", "1", "LOCAL"))

    def test_parser_rejects_duplicate_paths(self):
        with self.assertRaisesRegex(SceneParseError, "duplicate path"):
            parse_scene_text("/route/a ON\n/route/a OFF\n")

    def test_parser_rejects_non_path_content(self):
        with self.assertRaisesRegex(SceneParseError, "does not start"):
            parse_scene_text("run-this-command\n")

    def test_parser_rejects_missing_value(self):
        with self.assertRaisesRegex(SceneParseError, "has no value"):
            parse_scene_text("/config/path\n")

    def test_parser_enforces_size_boundary(self):
        with self.assertRaisesRegex(SceneParseError, "size limit"):
            parse_scene_text("/a 1", max_chars=3)


if __name__ == "__main__":
    unittest.main()
