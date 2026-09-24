import json
import tempfile
import unittest
from pathlib import Path

from av_validator.catalog import RuleCatalogError, load_rules
from av_validator.engine import evaluate_rules
from av_validator.integrity import SceneArtifact
from av_validator.reporting import build_report, format_text_report


class CatalogAndReportingTests(unittest.TestCase):
    def test_catalog_binds_expected_value_from_baseline(self):
        payload = {
            "rules": [
                {
                    "id": "R-001",
                    "name": "Main output",
                    "path": "/route/main",
                    "severity": "critical",
                    "rationale": "Protected route",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rules.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            rules, digest = load_rules(path, {"/route/main": ("ON",)})
        self.assertEqual(rules[0].expected, ("ON",))
        self.assertEqual(len(digest), 64)

    def test_catalog_rejects_path_missing_from_baseline(self):
        payload = {
            "rules": [
                {
                    "id": "R-001",
                    "name": "Main output",
                    "path": "/route/main",
                    "severity": "critical",
                    "rationale": "Protected route",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rules.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(RuleCatalogError, "baseline does not define"):
                load_rules(path, {})

    def test_report_contains_explainable_evidence(self):
        candidate = SceneArtifact(Path("candidate.scn"), "", 0, "a" * 64)
        baseline = SceneArtifact(Path("baseline.scn"), "", 0, "b" * 64)
        payload = {
            "rules": [
                {
                    "id": "R-001",
                    "name": "Main output",
                    "path": "/route/main",
                    "severity": "critical",
                    "rationale": "Protected route",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rules.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            rules, digest = load_rules(path, {"/route/main": ("ON",)})
        findings = evaluate_rules({"/route/main": ("OFF",)}, rules)
        report = build_report(candidate, baseline, findings, rule_count=1, rules_sha256=digest)
        text = format_text_report(report)
        self.assertIn("Expected: ON", text)
        self.assertIn("Observed: OFF", text)
        self.assertIn("[CRITICAL]", text)


if __name__ == "__main__":
    unittest.main()
