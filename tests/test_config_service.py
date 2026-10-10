import os
import unittest
from pathlib import Path
from unittest.mock import patch

from av_validator.config import ConfigurationError, Settings
from av_validator.service import validate_configuration


class ConfigurationAndServiceTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[1]
        self.baseline = self.root / "sample-configs/sanitized/approved-baseline.scn"
        self.rules = self.root / "rules/demo_rules.json"

    def test_settings_load_supported_environment_values(self):
        with patch.dict(
            os.environ,
            {
                "AV_VALIDATOR_MAX_SCENE_BYTES": "4096",
                "AV_VALIDATOR_OUTPUT_FORMAT": "json",
            },
            clear=True,
        ):
            settings = Settings.from_env()
        self.assertEqual(settings.max_scene_bytes, 4096)
        self.assertEqual(settings.output_format, "json")

    def test_settings_reject_invalid_environment_values(self):
        with (
            patch.dict(
                os.environ, {"AV_VALIDATOR_MAX_SCENE_BYTES": "many"}, clear=True
            ),
            self.assertRaisesRegex(ConfigurationError, "positive integer"),
        ):
            Settings.from_env()
        with (
            patch.dict(os.environ, {"AV_VALIDATOR_MAX_SCENE_BYTES": "0"}, clear=True),
            self.assertRaisesRegex(ConfigurationError, "positive integer"),
        ):
            Settings.from_env()
        with (
            patch.dict(os.environ, {"AV_VALIDATOR_OUTPUT_FORMAT": "xml"}, clear=True),
            self.assertRaisesRegex(ConfigurationError, "text or json"),
        ):
            Settings.from_env()

    def test_service_integrates_all_modules_for_drift_and_compliance(self):
        drift = validate_configuration(
            self.root / "sample-configs/sanitized/candidate-drift.scn",
            self.baseline,
            self.rules,
        )
        compliant = validate_configuration(
            self.root / "sample-configs/sanitized/candidate-compliant.scn",
            self.baseline,
            self.rules,
        )
        self.assertEqual(drift["status"], "findings")
        self.assertEqual(drift["summary"]["finding_count"], 4)
        self.assertEqual(compliant["status"], "compliant")
        self.assertEqual(compliant["summary"]["finding_count"], 0)


if __name__ == "__main__":
    unittest.main()
